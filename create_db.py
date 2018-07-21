import psycopg2

connection = psycopg2.connect(
    "dbname='ride_db' user='postgres' host='localhost'\
     password='15december' port ='5432'")
cursor = connection.cursor()

cursor.execute('CREATE DATABASE ride_db;')