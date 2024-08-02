import psycopg2

def create_db(conn):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(15) NOT NULL,
        last_name VARCHAR(15) NOT NULL,
        email VARCHAR(40) UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone_numbers(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES cient(id),
        phone VARCHAR(15)
    );
    """)

def add_client(conn, first_name, last_name, email, phones=None):
    cur.execute("""
        INSERT INTO clients (first_name, last_name, email)
        VALUES (%s, %s, %s) RETURNING id;
                """, (first_name, last_name, email))

def add_phone(conn, client_id, phone):
    cursor.execute("""
        INSERT INTO phone_numbers (client_id, phone_number)
        VALUES (%s, %s);
        """, (client_id, phone))

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    if first_name:
        cur.execute("UPDATE clients SET first_name = %s WHERE id = %s;", (first_name, client_id))
    if last_name:
        cur.execute("UPDATE clients SET last_name = %s WHERE id = %s;", (last_name, client_id))
    if email:
        cur.execute("UPDATE clients SET email = %s WHERE id = %s;", (email, client_id))

def delete_phone(cur, client_id, phone):
    cur.execute("""
        DELETE FROM phone_numbers WHERE client_id = %s AND phone = %s;
        """, (client_id, phone))

def delete_client(cur, client_id):
    # Сначала удаляем телефон
    cur.execute("""DELETE FROM phone_numbers WHERE client_id = %s;""", (client_id,))
    # Потом удаляем пользоваться
    cur.execute("DELETE FROM clients WHERE id = %s;", (client_id,))

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    query = '''
            SELECT c.id, c.first_name, c.last_name, c.email, p.phone
            FROM clients c LEFT JOIN phone_numbers p ON c.id = p.client_id
            WHERE TRUE
            '''
    params = []

    if first_name:
        query += ' AND c.first_name = %s;', (first_name,)
        params.append(first_name)
    if last_name:
        query += ' AND c.last_name = %s;', (last_name,)
        params.append(last_name)
    if email:
        query += ' AND c.email = %s;', (email,)
        params.append(email)
    if phone:
        query += ' AND p.phone = %s;', (phone,)
        params.append(phone)

    cur.execute(query, params)
    return cur.fetchall()

if __name__ == "__main__":
    conn = psycopg2.connect(database="netology_db", user="postgres", password="QwerAE86")
    with conn.cursor() as cur:
        # Создаем базу
        create_db(conn)

        # Добавляем клиентов
        client_id1 = add_client(conn, 'Nick', 'Smith', 'work_email@mail.com', ['521-373-7812'])
        client_id2 = add_client(conn, 'Alice', 'Loppes', 'aloppes@gmail.com', ['111-111-1111'])
        client_id3 = add_client(conn, 'Michael', 'CLinton', 'michaelworkspace@yahoo.com', ['657-988-5546'])

        # Изменяем клиента
        change_client(conn, client_id1, email='nicksmith@mail.com', phones=['123-456-7890'])

        # Добавляем номер клиенту
        add_phone(conn, client_id2, '736-132-7652')

        # Удаляем номер телефона
        delete_phone(conn, client_id3, '657-988-5546')

        # Удаляем пользователя
        delete_client(conn, client_id3)

        # Ищем клиента
        clients = find_client(conn, first_name='Alice')
        for client in clients:
            print(client)

        # Ищем клиента
        clients = find_client(conn, last_name='Smith')
        for client in clients:
            print(client)
    conn.close()