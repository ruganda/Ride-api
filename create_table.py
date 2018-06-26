import psycopg2

connection = psycopg2.connect(
    "dbname='ride_db' user='postgres' host='localhost' password='15december' port ='5432'")
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name text, username text, password text, rides_taken INTEGER, rides_given INTEGER )"
cursor.execute(create_table)