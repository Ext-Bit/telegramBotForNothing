from mysql.connector import Error, connect

def create_db_connection():
    connection = None
    cursor = None
    try:
        connection = connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'myDataBase'
        )
        cursor = connection.cursor()
    except Error as e:
        print(e)
    return [connection, cursor]