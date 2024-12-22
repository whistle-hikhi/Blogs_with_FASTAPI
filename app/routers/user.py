import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.post("/users",status_code=status.HTTP_201_CREATED ,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())

    # hash password
    hashed_password = utils.hash(user.password)
    new_user.password = hashed_password

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} was not found")
    return user