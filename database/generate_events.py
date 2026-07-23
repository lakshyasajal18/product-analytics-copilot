import random
import sqlite3
from datetime import datetime, timedelta

random.seed(42)

connection = sqlite3.connect("data/product_analytics.db")
cursor = connection.cursor()

cursor.execute("SELECT user_id, signup_date, device FROM users")
users = cursor.fetchall()

for user_id, signup_date, device in users:
    signup_datetime = datetime.fromisoformat(
        signup_date.replace("Z", "+00:00")
    )

    # Not every user starts a free trial.
    starts_trial = random.random() < 0.70

    if not starts_trial:
        continue

    trial_timestamp = signup_datetime + timedelta(
        days=random.randint(0, 7)
    )

    cursor.execute(
        """
        INSERT INTO events (user_id, event_type, event_timestamp)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            "started_trial",
            trial_timestamp.isoformat(),
        ),
    )

    # Desktop users convert slightly better than mobile users.
    conversion_probability = 0.45 if device == "Desktop" else 0.30

    subscribes = random.random() < conversion_probability

    if subscribes:
        subscription_timestamp = trial_timestamp + timedelta(
            days=random.randint(1, 14)
        )

        cursor.execute(
            """
            INSERT INTO events (user_id, event_type, event_timestamp)
            VALUES (?, ?, ?)
            """,
            (
                user_id,
                "subscribed",
                subscription_timestamp.isoformat(),
            ),
        )

connection.commit()
connection.close()

print("Trial and subscription events generated successfully!")