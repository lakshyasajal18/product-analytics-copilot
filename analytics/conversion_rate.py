import sqlite3

connection = sqlite3.connect("data/product_analytics.db")
cursor = connection.cursor()

cursor.execute("""
SELECT
    COUNT(DISTINCT CASE
        WHEN event_type = 'subscribed' THEN user_id
    END) AS subscribed_users,

    COUNT(DISTINCT CASE
        WHEN event_type = 'started_trial' THEN user_id
    END) AS trial_users

FROM events
""")

subscribed_users, trial_users = cursor.fetchone()

conversion_rate = (
    subscribed_users / trial_users * 100
    if trial_users > 0
    else 0
)

connection.close()

print(f"Trial users: {trial_users}")
print(f"Subscribed users: {subscribed_users}")
print(f"Conversion rate: {conversion_rate:.2f}%")