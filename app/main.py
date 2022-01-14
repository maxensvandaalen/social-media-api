from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .database import get_db
from . import models, schemas

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()
