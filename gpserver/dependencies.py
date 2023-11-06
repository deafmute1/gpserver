from database import connection as database

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def check_auth(): 
    pass