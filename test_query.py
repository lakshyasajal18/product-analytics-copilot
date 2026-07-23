from app.sql_generator import generate_sql
from database.query_database import execute_query

question = "How many users subscribed?"

# Step 1: Generate SQL
sql = generate_sql(question)

print("Generated SQL:")
print(sql)

# Step 2: Execute SQL
results = execute_query(sql)

print("\nResults:")
print(results)