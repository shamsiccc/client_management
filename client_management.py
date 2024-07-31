import psycopg2

with psycopg2.connect(database="netology_db", user="postgres", password="QwerAE86") as conn:
    with conn.cursor() as cur:

        # удаление таблиц
        # cur.execute("""
        # DROP TABLE phone_numbers;
        # DROP TABLE clients;
        # """)

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
            conn.commit

        def add_client(conn, first_name, last_name, email, phones=None):
            cur.execute("""
                INSERT INTO clients (first_name, last_name, email)
                VALUES (%s, %s, %s) RETURNING id;
                """, (first_name, last_name, email))
            conn.commit()

        def add_phone(conn, client_id, phone):
            cursor.execute("""
                INSERT INTO phone_numbers (client_id, phone_number)
                VALUES (%s, %s);
                """, (client_id, phone))
            conn.commit()

        def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
            if first_name:
                cur.execute("""UPDATE clients SET first_name = %s WHERE id = %s;""", (first_name, client_id))
            if last_name:
                cur.execute("""UPDATE clients SET last_name = %s WHERE id = %s;""", (last_name, client_id))
            if email:
                cur.execute("""UPDATE clients SET email = %s WHERE id = %s;""", (email, client_id))

            cur.execute("""DELETE FROM phone_numbers WHERE clients_id = %s;""", (client_id))
            cur.fetchall()

            if phone_numbers:
                for phone in phone_numbers:
                    add_phone(conn, client_id, phone)
            conn.commit()

        def delete_phone(conn, client_id, phone):
            cursor.execute("""DELETE FROM phone_numbers WHERE client_id = %s AND phone_number = %s;""", (client_id, phone))
            conn.commit()

        def delete_client(conn, client_id):
            cursor.execute("""DELETE FROM clients WHERE id = %s;""", (client_id,))
            conn.commit()

        def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
            query = '''
                    SELECT c.id, c.first_name, c.last_name, c.email, p.phone_number
                    FROM clients c LEFT JOIN phone_numbers p ON c.id = p.client_id
                    WHERE TRUE
                    '''
            params = []

            if first_name:
                query += ' AND c.first_name = %s'
                params.append(first_name)
            if last_name:
                query += ' AND c.last_name = %s'
                params.append(last_name)
            if email:
                query += ' AND c.email = %s'
                params.append(email)
            if phone:
                query += ' AND p.phone_number = %s'
                params.append(phone)

            cur.fetchall()


if __name__ == "__main__":
    with psycopg2.connect(database="netology_db", user="postgres", password="QwerAE86") as conn:
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