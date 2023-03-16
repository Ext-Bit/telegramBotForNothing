from create_connection import create_db_connection

def create_table():
    conn, cursor = create_db_connection()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        id INT UNIQUE,
                        username TEXT,
                        name TEXT,
                        age TEXT,
                        step INT,
                        state INT,
                        game_state TEXT,
                        photo INT DEFAULT 0,
                        amount_predictions INT DEFAULT 0,
                        date DATE,
                        access_level INT DEFAULT 0,
                        companion_id INT DEFAULT 0,
                        request_companion INT DEFAULT 0
                        )''')

    conn.commit()
    cursor.close()
    conn.close()


def delete_table():
    conn, cursor = create_db_connection()

    cursor.execute('DROP TABLE users')

    conn.commit()
    cursor.close()
    conn.close()

var = None
while var != 2:
    var = int(input('0 - удалить таблицу\n1 - создать таблицу\n2 - stop\n: '))
    if var == 0:
        delete_table()
    elif var == 1:
        create_table()
