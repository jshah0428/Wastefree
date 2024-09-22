# Import necessary libraries
import sqlite3
import matplotlib.pyplot as plt
import datetime

# Define constants
NUM_DAYS = 15

# Connect to database
conn = sqlite3.connect('../recipe.db')
cursor = conn.cursor()

# Fetch data for the past 15 days
cursor.execute('''
    SELECT purchase_date, wasted, total_price 
    FROM pantry 
    WHERE purchase_date >= DATE('now', '-{} days')
    ORDER BY purchase_date ASC
'''.format(NUM_DAYS))
data = cursor.fetchall()

# Extract dates and values
dates = [datetime.datetime.strptime(row[0], '%Y-%m-%d').date() for row in data]
wasted_values = [row[1] for row in data]
total_price_values = [row[2] for row in data]

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Plot wasted values
ax.plot(dates, wasted_values, marker='o', label='Waste')
ax.set_xlabel('Date')
ax.set_ylabel('Wastage')

# Plot total price values
ax2 = ax.twinx()
ax2.plot(dates, total_price_values, marker='s', color='r', label='Total Price')
ax2.set_ylabel('Total Price')

# Set titles and labels
ax.set_title('Waste and Price Over Time')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

# Rotate x-axis labels
ax.tick_params(axis='x', rotation=90)

# Set limits
current_date = datetime.date.today()
last_date = current_date - datetime.timedelta(days=NUM_DAYS)
ax.set_xlim([last_date, current_date])

# Layout so plots do not overlap
fig.tight_layout()

# Save the plot as an image and return the file path
image_path = '../waste_price_plot.png'
plt.savefig(image_path)

# Close the plot
plt.close(fig)

# Return the image path
print(f"Plot saved at: {image_path}")
