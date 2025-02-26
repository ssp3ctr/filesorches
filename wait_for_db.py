import time
import psycopg2
import os

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "file_metadata_storage")
DB_USER = os.getenv("POSTGRES_USER", "postgre")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123123")


def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
            )
            conn.close()
            print("✅ Database is ready!")
            break
        except Exception as e:
            print(f"⏳ Waiting for database... Error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    wait_for_db()
