from fastapi import Depends, FastAPI

from .oauth2 import get_current_user
from .schemas import User
from .routers import auth, comment, post, user

app = FastAPI()
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)


@app.get("/")
async def root(current_user: User = Depends(get_current_user)):
    return {"message": "Hello World"}
