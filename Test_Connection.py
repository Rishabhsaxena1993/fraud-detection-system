import mysql.connector

# MySQL se connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",           # apna username yahan daal
    password="Rishabh@1993",  # apna password yahan daal
    database="fraud_detection"
)

cursor = conn.cursor()

# Data fetch karna
cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

# Print karna
for row in rows:
    print(row)

# Close karna
cursor.close()
conn.close()
