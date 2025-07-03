from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URL = "postgresql://postgres:gopiPostgre@localhost/fastapi_db"

engine = create_engine(DATABASE_URL)

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Connection successful:", result.scalar())
    except SQLAlchemyError as e:
        print("Connection failed:", str(e))

test_connection()
