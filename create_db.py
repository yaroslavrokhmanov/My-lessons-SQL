import mysql.connector

# Подключение к MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="242187"
)

cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS postwall_db")
cursor.close()
connection.close()

