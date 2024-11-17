import os

from dotenv import load_dotenv

load_dotenv(
    dotenv_path='.env',
    verbose=True,
    encoding='utf-8',
)

BOT_TOKEN = os.environ['BOT_TOKEN']

DB_CONNECTION = {
    'host': os.environ['DB_HOST'],
    'dbname': os.environ['DB_DATABASE'],
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
}