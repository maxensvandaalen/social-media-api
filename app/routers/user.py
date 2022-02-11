from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import get_password_hash


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_names = db.query(models.User.name).all()
    user_emails = db.query(models.User.email).all()

    if user.name in [value for value, in user_names]:
        raise HTTPException(status_code=409, detail="this username is already registered")
    
    if user.email in [value for value, in user_emails]:
        raise HTTPException(status_code=409, detail="this emailadress is already registered")

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())       
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
