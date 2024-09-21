from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class LoginScreen(BoxLayout):
    feedback = StringProperty('')

    def do_login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        # Simple authentication logic (replace with real authentication)
        if username == 'admin' and password == 'password':
            self.feedback = 'Login successful!'
        else:
            self.feedback = 'Invalid username or password.'


class LoginApp(App):
    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    LoginApp().run()
