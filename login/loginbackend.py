import sqlite3
import bcrypt
import os
import re  # For regular expressions
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

# Path to your SQLite database file
DATABASE_NAME = 'wastefree_db.db'


def initialize_database():
    if not os.path.exists(DATABASE_NAME):
        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        connection.commit()
        connection.close()


def is_valid_username(username):
    # Username must be 3-20 characters long and can contain letters, numbers, underscores, and periods
    return re.match("^[A-Za-z0-9_.]{3,20}$", username) is not None


def is_valid_email(email):
    # Simple regex for email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def is_valid_password(password):
    # Password must be at least 6 characters long
    return len(password) >= 6


class LoginScreen(Screen):
    feedback = StringProperty('')

    def do_login(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()

        if not username or not password:
            self.feedback = 'Please enter both username and password.'
            return

        if not os.path.exists(DATABASE_NAME):
            self.feedback = 'Database not found.'
            return

        # Connect to the SQLite database
        try:
            connection = sqlite3.connect(DATABASE_NAME)
            cursor = connection.cursor()

            # Query the user table for the given username
            cursor.execute('''
                SELECT password FROM user WHERE username = ?
            ''', (username,))
            result = cursor.fetchone()

            if result:
                stored_password = result[0]

                # Verify the password using bcrypt
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    self.feedback = ''
                    # TODO: Navigate to the main app screen or perform other actions
                    print('Login successful!')
                else:
                    self.feedback = 'Invalid username or password.'
            else:
                self.feedback = 'Invalid username or password.'

        except Exception as e:
            self.feedback = 'An error occurred during authentication.'
            print(f"Database error: {e}")
        finally:
            if 'connection' in locals():
                connection.close()

    def go_to_register(self):
        self.manager.current = 'registration_screen'


class RegistrationScreen(Screen):
    feedback = StringProperty('')

    def do_register(self):
        first_name = self.ids.first_name_input.text.strip()
        last_name = self.ids.last_name_input.text.strip()
        email = self.ids.email_input.text.strip()
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()

        if not all([first_name, last_name, email, username, password]):
            self.feedback = 'Please fill in all fields.'
            return

        # Validate email
        if not is_valid_email(email):
            self.feedback = 'Invalid email format.'
            return

        # Validate username
        if not is_valid_username(username):
            self.feedback = ('Invalid username. Must be 3-20 characters long and can contain letters, '
                             'numbers, underscores, or periods.')
            return

        # Validate password
        if not is_valid_password(password):
            self.feedback = 'Password must be at least 6 characters long.'
            return

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to the database and insert the new user
        try:
            connection = sqlite3.connect(DATABASE_NAME)
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO user (first_name, last_name, email, username, password)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, username, hashed_password.decode('utf-8')))

            connection.commit()
            self.feedback = 'User registered successfully.'
            # Navigate back to the login screen
            self.manager.current = 'login_screen'
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed: user.username' in str(e):
                self.feedback = 'Username already exists.'
            elif 'UNIQUE constraint failed: user.email' in str(e):
                self.feedback = 'Email already registered.'
            else:
                self.feedback = 'Integrity error during registration.'
            print(f"Integrity error: {e}")
        except Exception as e:
            self.feedback = 'An error occurred during registration.'
            print(f"Database error: {e}")
        finally:
            if 'connection' in locals():
                connection.close()


class LoginApp(App):
    def build(self):
        initialize_database()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(RegistrationScreen(name='registration_screen'))
        return sm


if __name__ == '__main__':
    LoginApp().run()
