import psycopg
import os


def start_connection():
  connection = psycopg.connect(
      host=os.getenv("DB_HOST"),
      port=5432,
      dbname=os.getenv("DB_NAME"),
      user=os.getenv("DB_USER"),
      password=os.getenv("DB_PASSWORD"),
  )

  print("PostgreSQL connected successfully!")

  connection.close()
