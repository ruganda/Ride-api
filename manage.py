import os
import psycopg2
from app import create_app
from app.database import Database

app = create_app('PRODUCTION')
db = Database(os.getenv("DATABASE_URL"))

if __name__ == '__main__':
    db.create_database(os.getenv('DB_NAME'))
    db.create_tables()
    app.run(debug=True)
