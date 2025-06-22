from sqlalchemy import create_engine, text
from app.config.settings import settings

def get_db_engine():
    return create_engine(settings.DATABASE_URL)

def execute_sql_query(query: str, params: dict = None):
    engine = get_db_engine()
    with engine.connect() as connection:
        result = connection.execute(text(query), params if params else {})
        return result.mappings().all()
