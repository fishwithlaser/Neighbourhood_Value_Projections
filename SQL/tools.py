from sqlalchemy import create_engine

def get_engine():
    return create_engine('sqlite:///SQL/database.db', echo=True)


    
