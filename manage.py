import os
import psycopg2
from app import create_app
from app.database import Database

app = create_app('PRODUCTION')
db = Database('postgres://xmgdymngkwtqzl:29fa7e2b61e50a08cd256f312cbc59af3a972126f772016ded78355e87a121aa@ec2-50-19-86-139.compute-1.amazonaws.com:5432/d71q4cvgvtvqck')

if __name__ == '__main__':
    db.create_database('d71q4cvgvtvqck')
    db.create_tables()
    app.run(debug=True)
