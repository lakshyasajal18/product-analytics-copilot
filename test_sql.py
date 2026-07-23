from app.sql_generator import generate_sql

question = "How many users subscribed?"

sql = generate_sql(question)

print(sql)