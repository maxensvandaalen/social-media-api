from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=list[schemas.Comment])
def get_all_comments(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return db.query(models.Comment).all()
