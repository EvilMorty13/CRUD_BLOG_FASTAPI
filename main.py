from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlowClientCredentials
from contextlib import asynccontextmanager
from blog_app.users.routes import user_router
from blog_app.posts.routes import post_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

app = FastAPI()


app.include_router(user_router)
app.include_router(post_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the blog application!"}
