from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=list[schemas.Comment])
def get_all_comments(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return db.query(models.Comment).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {comment.post_id} does not exist")

    db_comment = models.Comment(
        owner_id=current_user.id, **comment.dict()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
