from fastapi import APIRouter


router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
) 

@router.post("/create-user")
def create_user(
    
): 
    pass
