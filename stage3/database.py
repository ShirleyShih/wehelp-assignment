from fastapi import *
import mysql.connector
import os

RDS_PASSWORD = os.environ.get('AWS_ACCESS_KEY_ID')
print(RDS_PASSWORD)

db_config = {
    'user': 'admin',
    'password': os.environ.get('AWS_ACCESS_KEY_ID'),
    'host': 'wehelpstage34.cb280weeg64t.us-west-2.rds.amazonaws.com',
    'database': 'wehelpstage3'
}

con = mysql.connector.connect(**db_config)
cursor = con.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stage3 (
        message_id bigint primary key auto_increment,
        textContent varchar(255) not null,
        imageURL varchar(255) not null
    )
""")

con.commit()
cursor.close()