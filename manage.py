import os
import psycopg2
from app import create_app
from app.database import Database

app = create_app('PRODUCTION')
db = Database('postgres://akcolxjufhesko:d01b99b7009c67760234fb1bcb4229e5566490f2e125fc4b539e5d83ee14fbae@ec2-23-21-216-174.compute-1.amazonaws.com:5432/d6bbirccjc7b3e')

if __name__ == '__main__':
    # db.create_database('ride_db')
    db.create_tables()
    # port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)
