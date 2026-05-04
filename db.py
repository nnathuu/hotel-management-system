import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Nnat070206",
        database="hotelmanagement"
    )