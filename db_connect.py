import mysql.connector
from mysql.connector.errors import Error

# Create a connection to the MySQL database
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="pdfx",
        port="3306"
    )
    print("Connection successful")

except Error as e:
    print(f"The error '{e}' occurred")
    mydb = None

if mydb is not None:
    # Create a cursor to execute SQL queries
    mycursor = mydb.cursor()
else:
    print("Connection failed")