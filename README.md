# Product Analytics Copilot

Product Analytics Copilot is an AI-powered analytics assistant that allows users to explore product data using natural language. Instead of writing SQL manually, users can ask questions in plain English, and the application generates SQL, executes it on a SQLite database, visualizes the results, and provides AI-generated business insights.

## Features

- Ask questions about product data in natural language
- Automatically generate SQL queries using Gemini
- Execute queries against a SQLite database
- Automatically visualize results with the most appropriate chart
- Generate AI-powered summaries, insights, and recommendations
- Interactive dashboard built with Streamlit

## Example Questions

- What is the conversion rate?
- Show subscribed users by device.
- Show the distribution of trial users by country.
- Show subscriptions over time.

## Tech Stack

- Python
- Streamlit
- SQLite
- Gemini API
- Pandas
- Altair

## Project Structure

```text
product-analytics-copilot/
│
├── app/
│   ├── main.py
│   ├── sql_generator.py
│   └── insight_generator.py
│
├── analytics/
├── database/
├── data/
│
├── requirements.txt
└── README.md
```

## How It Works

1. The user asks a question in natural language.
2. Gemini converts the question into a SQL query.
3. The query is executed against a SQLite database.
4. The results are displayed as a table, metric, or chart.
5. Gemini generates a concise business summary, insight, and recommendation.

## Running the Project

Clone the repository:

```bash
git clone https://github.com/yourusername/product-analytics-copilot.git
cd product-analytics-copilot
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key
```

Run the application:

```bash
python -m streamlit run app/main.py
```

## Future Improvements

- Support additional databases such as PostgreSQL
- More advanced product analytics metrics
- Dashboard customization
- Conversation history
- Deploy as a web application

## Author

Lakshya SK
