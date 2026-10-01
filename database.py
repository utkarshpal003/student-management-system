import mysql.connector
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_connection():
    url = os.getenv("MYSQL_PUBLIC_URL")

    if not url:
        raise Exception("MYSQL_PUBLIC_URL environment variable is missing")

    parsed = urlparse(url)

    connection = mysql.connector.connect(
        host=parsed.hostname,
        port=parsed.port or 3306,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path.lstrip("/")
    )

    return connection

