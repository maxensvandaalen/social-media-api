from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@router.get("/{post_id}", response_model=schemas.Post )
def read_post_by_id(post_id: int, db: Session = Depends(get_db)):
    return db.query(models.Post).filter(models.Post.id == post_id).first()