from fastapi import APIRouter


router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
) 

# enforce utf8 on usernames

@router.post("/create-user")
def create_user(
    
): 
    pass
