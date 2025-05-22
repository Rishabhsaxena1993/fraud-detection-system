import mysql

from app.db.connection import get_connection
from mysql.connector import Error

def init_db():
    try:
        # Connect without database first to create it
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Rishabh@1993"  # Yaha apna password rakh
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS fraud_detection")
        conn.commit()
        cursor.close()
        conn.close()

        # Now connect to the database and create table
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                city VARCHAR(100),
                country VARCHAR(100),
                fraud_code INT
            )
        """)
        conn.commit()
        print("Database and table initialized successfully!")
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    init_db()