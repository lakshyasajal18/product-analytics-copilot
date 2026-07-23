from dotenv import load_dotenv
import os
from google import genai

# Load environment variables
load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Database schema and instructions for Gemini
SCHEMA = """
You are an expert SQLite analyst.

Convert the user's question into one valid SQLite SELECT query.

Database schema:

users(
    user_id INTEGER,
    name TEXT,
    country TEXT,
    device TEXT,
    signup_date TEXT
)

events(
    event_id INTEGER,
    user_id INTEGER,
    event_type TEXT,
    event_timestamp TEXT
)

Valid event_type values:
- started_trial
- subscribed

Rules:
1. Return only the SQL query.
2. Do not use markdown.
3. Do not include explanations.
4. Only generate SELECT queries.
5. Use SQLite-compatible syntax.
6. Use COUNT(DISTINCT user_id) when counting users.
7. For subscription questions, filter event_type = 'subscribed'.
8. For trial questions, filter event_type = 'started_trial'.
9. For conversion rate, calculate:
   subscribed users / trial users * 100.
10. If the user asks "over time" without specifying a period, group by month.

11. Use these SQLite date functions:
    - Day: DATE(event_timestamp)
    - Week: STRFTIME('%Y-%W', event_timestamp)
    - Month: STRFTIME('%Y-%m', event_timestamp)
    - Year: STRFTIME('%Y', event_timestamp)

12. When grouping by time:
    - SELECT the formatted date as an alias (day, week, month, or year)
    - GROUP BY the exact same expression
    - ORDER BY the exact same expression

13. Example for "subscriptions over time":

SELECT
    STRFTIME('%Y-%m', event_timestamp) AS month,
    COUNT(DISTINCT user_id) AS subscribed_users
FROM events
WHERE event_type = 'subscribed'
GROUP BY STRFTIME('%Y-%m', event_timestamp)
ORDER BY STRFTIME('%Y-%m', event_timestamp);

14. Always use meaningful column aliases such as:
    month
    week
    day
    year
    subscribed_users
    trial_users
    total_users

User question:
{question}
"""


def generate_sql(question: str):
    prompt = f"""
{SCHEMA}

User question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text.strip()
