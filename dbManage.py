# connect to the PostgreSQL database
from datetime import datetime
import psycopg2 as psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="NewsFactCheck",
    user="admin",
    password="P@ssw0rd"
)

def save_record():
    cur = conn.cursor()
    cur.execute("INSERT INTO records(user_name, article_content, record_date, accuracy, source_link, remark) VALUES (%s, %s, %s, %s, %s, %s);",
                ("admin", "test1", datetime.now(), 90.99, "test_link", "test"))
    conn.commit()