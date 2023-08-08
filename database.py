import psycopg2
from datetime import datetime
from psycopg2 import Error
from psycopg2 import DATETIME
from psycopg2.extras import RealDictCursor
from HangmanGame import HangmanGame


def init_db():
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="hangman_game")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        cursor.execute('''
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
        connection.commit()

        # Close communication with the database
        cursor.close()
        connection.close()
    except Error as e:
        print('error: ' + str(e))


def create_game(attempts, word, username) -> int:
    current_word = '_' * len(word)
    game_state = 'ongoing'
    time_created = datetime.now()
    time_updated = time_created

    conn = psycopg2.connect(user="postgres",
                            password="postgres",
                            host="127.0.0.1",
                            port="5432",
                            database="hangman_game")


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


def get_game(id):
    # Connect to your postgres DB
    conn = psycopg2.connect(user="postgres",
                            password="postgres",
                            host="127.0.0.1",
                            port="5432",
                            database="hangman_game")

    # Open a cursor to perform database operations
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Execute the SELECT statement
    cur.execute("""
        SELECT * FROM public.game_state
        WHERE id = %s;
    """, (id,))

    # Fetch the result
    row = cur.fetchone()

    # Close communication with the database
    cur.close()
    conn.close()

    return row


def update_game(id, attempts, current_word, game_status):
    time_updated = datetime.now()
    conn = psycopg2.connect(user="postgres",
                            password="postgres",
                            host="127.0.0.1",
                            port="5432",
                            database="hangman_game")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute the INSERT statement
    cur.execute(f'''

UPDATE public.game_state
SET attempts = {attempts},
    current_word = '{current_word}',
    time_updated = {time_updated},
    game_status = '{game_status}'
WHERE id = {id};
                ''')

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()


try:
    init_db()
    id = create_game(6, 'cat', 'Alex')
    game = get_game(id)
    for entry in game:
        print(entry + ': ' + str(game[entry]))

    update_game(id, 5, '___', 'ongoing')

    game = get_game(id)
    for entry in game:
        print(entry + ': ' + str(game[entry]))

except Error as e:
    print(e)
