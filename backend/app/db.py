from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
load_dotenv()
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/safecity')
engine = create_engine(DB_URL, future=True)
def run_query(q, params=None):
    with engine.connect() as conn:
        return conn.execute(text(q), params or {})
