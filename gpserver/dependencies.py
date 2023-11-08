from datetime import datetime
from secrets import compare_digest
from fastapi import Request, status
from .database import connection 

## Dependencies

def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def check_auth(request: Request): 
    pass