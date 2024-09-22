import sqlite3

db_connect = '/Users/shreyaskonanki/PycharmProjects/Wastefree/recipe.db'

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


def pantry_database():
    connection = sqlite3.connect(db_connect)
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pantry (
        id INTEGER PRIMARY KEY NOT NULL,                      -- Unique ID for each record in the pantry
        item_name TEXT,
        quantity INTEGER,
        unit_price REAL,
        total_price REAL,
        purchase_date DATETIME DEFAULT (CURRENT_TIMESTAMP),
        expiry_date DATE,
        consumed INTEGER DEFAULT 0,  -- 1 if consumed, 0 if wasted
        wasted INTEGER DEFAULT 0,     -- 1 if wasted, 0 if not
        FOREIGN KEY (id) REFERENCES user(id)  -- Foreign key to user table
);
    
    ''')
    connection.commit()
    connection.close()