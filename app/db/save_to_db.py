import pandas as pd
from app.db.database import get_db_engine
from sqlalchemy import inspect, text

def delete_all_tables():
    """Delete all tables in the database"""
    engine = get_db_engine()
    inspector = inspect(engine)
    
    with engine.connect() as connection:
        # Start a transaction
        with connection.begin():
            # Get all table names
            tables = inspector.get_table_names()
            
            for table in tables:
                print(f"Dropping table: {table}")
                # Drop table
                connection.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
        
        print(f"Dropped {len(tables)} tables")

def save_dataframe_to_db(df: pd.DataFrame, file_name: str):
    """Save DataFrame to PostgreSQL database"""
    # Delete all existing tables first
    delete_all_tables()
    
    engine = get_db_engine()
    table_name = clean_table_name(file_name)
    
    # Convert DataFrame column names to lowercase and replace spaces
    df.columns = [clean_column_name(col) for col in df.columns]
    
    print(f"Creating new table: {table_name}")
    # Save to database
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    return table_name


def clean_table_name(name: str) -> str:
    """Clean file name to valid table name"""
    return name.lower().replace('.', '_').replace(' ', '_')

def clean_column_name(name: str) -> str:
    """Clean column name to valid SQL column name"""
    return str(name).lower().replace(' ', '_').replace('-', '_')