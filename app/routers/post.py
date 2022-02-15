from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return db.query(models.Post).all()


@router.get("/{post_id}", response_model=schemas.Post)
def read_post_by_id(post_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} does not exist")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_post = models.Post(
        owner_id=current_user.id, **post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform the request")

    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(updated_post: schemas.PostCreate, post_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {post_id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform the request")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
