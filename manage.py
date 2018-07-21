import os
import psycopg2
from app import create_app
from app.database import Database

app = create_app('PRODUCTION')
db = Database('postgresql://postgres:15december@localhost:5432/ride_db')

if __name__ == '__main__':
    db.create_database('ride_db')
    db.create_tables()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
