import os

from dotenv import load_dotenv

load_dotenv()

APP_HOST = os.getenv("APP_HOST", default="localhost")
APP_PORT = os.getenv("APP_PORT", default=8000)
PG_HOST = os.getenv("PG_HOST", default="db")
PG_PORT = os.getenv("PG_PORT", default=5432)
PG_USER = os.getenv("PG_USER", default="postgres")
PG_PASS = os.getenv("PG_PASS", default="postgres")
PG_DBNAME = os.getenv("PG_DBNAME", default="wav2mp3")
SQLALCHEMY_DB_CONN_STRING = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}/{PG_DBNAME}"
)
