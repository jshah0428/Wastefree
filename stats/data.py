import sqlite3
import pandas as pd
import numpy as np
from datetime import date, timedelta

# Connect to the database
conn = sqlite3.connect('/recipe.db')
cursor = conn.cursor()

# Get today's date
today = date.today()

# Set the current date around today's date
current_date = today - timedelta(days=np.random.randint(0, 30))

# Create a list of items
items = [
    'Apples',
    'Bananas',
    'Carrots',
    'Oranges',
    'Pineapple',
    'Tomatoes',
    'Milk',
    'Bread',
    'Eggs',
    'Chicken',
    'Pork',
    'Beef',
]

# Create a list of purchase dates
purchase_dates = [(current_date + timedelta(days=np.random.randint(0, 30))).isoformat() for _ in range(100)]

# Create a list of expiration dates
expiration_dates = [(today + timedelta(days=np.random.randint(7, 365))).isoformat() for _ in range(100)]

# Create a list of prices
prices = [np.random.uniform(1.0, 10.0) for _ in range(100)]

# Create a list of quantities
quantities = [np.random.randint(1, 10) for _ in range(100)]

# Create a list of wasted values (add some randomness)
wasted = [int(np.random.choice([0, 1], p=[0.8, 0.2])) for _ in range(100)]

# Create a pandas dataframe to store the fake data
df = pd.DataFrame({
    'id': range(1, 101),
    'item_name': np.random.choice(items, 100),
    'total_price': prices,
    'purchase_date': purchase_dates,
    'expiry_date': expiration_dates,
    'quantity': quantities,
    'wasted': wasted
})

# Loop through the dataframe and insert the fake data into the pantry table
for index, row in df.iterrows():
    cursor.execute('''
        INSERT INTO pantry (id, item_name, total_price, purchase_date, expiry_date, quantity, wasted)
        VALUES (?,?,?,?,?,?,?)
    ''', (row['id'], row['item_name'], row['total_price'], row['purchase_date'], row['expiry_date'], row['quantity'], row['wasted']))

# Commit the changes and close the connection
conn.commit()
conn.close()