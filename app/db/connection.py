# app/db/connection.py
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rishabh@1993",
        database="fraud_detection"
    )
