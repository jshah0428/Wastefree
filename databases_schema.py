import sqlite3

db_connect = '/Users/jainamshah/PycharmProjects/Wastefree/recipe.db'

def initialize_accounts_database():
    connection = sqlite3.connect(db_connect)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
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


def saved_recipes_db():
    connection = sqlite3.connect(db_connect)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SAVED_RECIPES(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            RECIPE_NAME VARCHAR(255) NOT NULL,
            RECIPE_URL VARCHAR(255),
            RECIPE_INGREDIENTS TEXT,
            RECIPE_DESCRIPTION TEXT,
            RECIPE_DIRECTIONS TEXT,
            RECIPE_NUTRITION TEXT,
            RECIPE_PREP_INFO TEXT,
            FOREIGN KEY (ID) REFERENCES user(id)
        );
    ''')
    connection.commit()
    connection.close()