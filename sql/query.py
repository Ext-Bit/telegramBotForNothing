from sql.create_connection import create_db_connection

def select(columns: list, table: str, terms = '', res = 'one'):
    conn, cursor = create_db_connection()
    columns_str = ', '.join(columns)
    if terms != '':
        cursor.execute(f'SELECT {columns_str} FROM {table} WHERE {terms}')
        res = cursor.fetchone()
        if res == 'one':
            res = cursor.fetchone()
        elif res == 'all':
            res = cursor.fetchall()
    else:
        cursor.execute(f'SELECT {columns_str} FROM {table}')
        res = cursor.fetchall()
    cursor.close()
    conn.close()
    print('query select done')
    return res


def update(table: str, parameters: list, user_id: int):
    conn, cursor = create_db_connection()
    parameters_str = ', '.join(parameters)
    print(f'UPDATE {table} SET {parameters_str} WHERE id = {user_id}')
    cursor.execute(f'UPDATE {table} SET {parameters_str} WHERE id = {user_id}')
    conn.commit()
    cursor.close()
    conn.close()
    print('query update done')


def insert(table: str, columns: list, values: list):
    conn, cursor = create_db_connection()
    count = ''
    columns_str = ', '.join(columns)
    for i in values:
        count += '%s, '
    cursor.execute(f'INSERT INTO {table}({columns_str}) VALUES({count[:-2]})', values)
    conn.commit()
    cursor.close()
    conn.close()
    print('query insert done')
