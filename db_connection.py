import mysql.connector
#Database credentials
def connect():
    return mysql.connector.connect(
        host="localhost",
        user="username",
        password="password",
        database="credentials"
    )
