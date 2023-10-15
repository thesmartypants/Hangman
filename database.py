import psycopg2
from datetime import datetime
from psycopg2 import Error
from psycopg2 import DATETIME
from psycopg2.extras import RealDictCursor


class Database:


    def __init__(self, conn_str: str):
        self.conn_str = conn_str

    # conn = psycopg2.connect(user="postgres",
    #                         password="postgres",
    #                         host="127.0.0.1",
    #                         port="5432",
    #                         database="hangman_game")

    def init_db(self):
        try:

            # Connect to an existing database

            # Create a cursor to perform database operations
            conn = psycopg2.connect(self.conn_str)
            cur = conn.cursor()
            cur.execute('''
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT FROM pg_tables
                    WHERE schemaname = 'public'
                    AND tablename   = 'game_state'
                ) THEN
                    CREATE TABLE public.game_state (
                        id serial primary key,
                        attempts int,
                        current_word varchar(255),
                        word varchar(255),
                        game_status varchar(255),
                        username  varchar(255),
                        time_created timestamp,
                        time_updated timestamp
                    );
                END IF;
            END $$;
            ''')
            conn.commit()

            # Close communication with the database
            cur.close()
            conn.close()
        except Error as e:
            print('error: ' + str(e))

    def create_game(self, attempts, word, username) -> int:
        try:
            current_word = '_' * len(word)
            game_state = 'ongoing'
            time_created = datetime.now()
            time_updated = time_created

            conn = psycopg2.connect(self.conn_str)

            # Open a cursor to perform database operations
            cur = conn.cursor()

            # Execute the INSERT statement
            cur.execute("""
                INSERT INTO public.game_state (attempts, current_word, word, game_status, username, time_created, time_updated)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (attempts, current_word, word, game_state, username, time_created, time_updated))

            # Get the generated id back
            id_of_new_row = cur.fetchone()[0]

            # Make the changes to the database persistent
            conn.commit()

            # Close communication with the database
            cur.close()
            conn.close()

            return id_of_new_row
        except Error as e:
            print('error: ' + str(e))

    ####
    def get_game(self, game_id):
        # Connect to your postgres DB
        conn = psycopg2.connect(self.conn_str)

        try:

            # Open a cursor to perform database operations
            cur = conn.cursor(cursor_factory=RealDictCursor)

            # Execute the SELECT statement
            cur.execute("""
                SELECT * FROM public.game_state
                WHERE id = %s;
            """, (game_id,))

            # Fetch the result
            row = cur.fetchone()

            # Close communication with the database
            cur.close()
            conn.close()

            return row
        except Error as e:
            print('error: ' + str(e))

        #####

    def update_game(self, game_id, attempts, current_word, game_status):

        time_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = psycopg2.connect(self.conn_str)

        # Open a cursor to perform database operations
        cur = conn.cursor()
        try:
            # Execute the UPDATE statement
            cur.execute('''
                    UPDATE public.game_state
                    SET attempts = %s,
                        current_word = %s,
                        time_updated = %s,
                        game_status = %s
                    WHERE id = %s;
                ''', (attempts, current_word, time_updated, game_status, game_id))

            # Make the changes to the database persistent
            conn.commit()

            # Close communication with the database
        except Error as e:
            print('error: ' + str(e))
        finally:
            cur.close()
            conn.close()

    def delete_all_tables(self):
        try:

            # Connect to an existing database

            # Create a cursor to perform database operations
            conn = psycopg2.connect(self.conn_str)
            cur = conn.cursor()
            cur.execute('''
               drop table public.game_state
               ''')
            conn.commit()

            # Close communication with the database
            cur.close()
            conn.close()
        except Error as e:
            print('error: ' + str(e))

