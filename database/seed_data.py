import random
import sqlite3

import requests

API_URL = "https://randomuser.me/api/?results=100&seed=learnflow"

response = requests.get(API_URL, timeout=30)
response.raise_for_status()

users = response.json()["results"]

connection = sqlite3.connect("data/product_analytics.db")
cursor = connection.cursor()

devices = ["Mobile", "Desktop"]

for user in users:

    user_id = user["login"]["uuid"]

    name = f"{user['name']['first']} {user['name']['last']}"

    country = user["location"]["country"]

    signup_date = user["registered"]["date"]

    device = random.choice(devices)

    cursor.execute(
        """
        INSERT INTO users
        (user_id, name, country, device, signup_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, name, country, device, signup_date),
    )

connection.commit()
connection.close()

print(f"Inserted {len(users)} users.")