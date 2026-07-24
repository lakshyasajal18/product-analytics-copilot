# Product Analytics Copilot
<img width="1499" height="681" alt="Screenshot 2026-07-24 at 12 30 30 PM" src="https://github.com/user-attachments/assets/dc4c32aa-cbc4-4377-baec-f236c4c7b83e" />

Product Analytics Copilot is an AI-powered analytics assistant that enables users to explore product data using natural language. Instead of writing SQL manually, users can ask business questions in plain English, and the application generates SQL using Google's Gemini API, executes it on a SQLite database, visualizes the results, and generates AI-powered business insights.

**Try it here!** 
https://analytics-copilot-lakshya.streamlit.app/

---

## Features

- Ask business questions in natural language
- Generate SQL queries using Google's Gemini API
- Execute queries against a SQLite database
- Automatically visualize results with the most appropriate chart
- Generate AI-powered summaries, insights, and recommendations
- Interactive dashboard built with Streamlit

---

## Example Questions

- What is the conversion rate?
- Show subscribed users by device.
- Show the distribution of trial users by country.
- Show subscriptions over time.

---

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- SQLite
- Pandas
- Altair

---

## Project Structure

```text
product-analytics-copilot/
│
├── analytics/
│   └── conversion_rate.py
│
├── app/
│   ├── main.py
│   ├── sql_generator.py
│   └── insight_generator.py
│
├── data/
│   └── product_analytics.db
│
├── database/
│   ├── setup_database.py
│   ├── seed_data.py
│   ├── generate_events.py
│   └── query_database.py
│
├── requirements.txt
└── README.md
```

---

## How It Works

1. Enter a business question in plain English.
2. Gemini converts the question into a SQL query.
3. The query is executed against the SQLite database.
4. Results are displayed as tables, metrics, or charts.
5. Generate an optional AI insight with a summary, interpretation, and recommendation.

---

## Getting Started

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/product-analytics-copilot.git
cd product-analytics-copilot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```text
GEMINI_API_KEY=your_api_key_here
```

Run the application:

```bash
streamlit run app/main.py
```

---

## Future Improvements

- Support additional databases such as PostgreSQL
- Export query results
- Conversation history
- User authentication
- Additional product analytics metrics

---

## Author

**Lakshya SK**
