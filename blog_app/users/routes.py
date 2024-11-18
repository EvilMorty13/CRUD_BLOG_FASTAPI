from fastapi import APIRouter, HTTPException, Depends
from passlib.hash import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pymongo.collection import Collection
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

from database import db
from blog_app.users.schemas import UserCreate,UserResponse,LoginRequest
from blog_app.users.models import User

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

user_router = APIRouter(prefix="/users", tags=["Users"])

users_collection: Collection = db["users"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@user_router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    user_data = {"username": user.username, "email": user.email, "hashed_password": hashed_password}
    users_collection.insert_one(user_data)
    return {"username": user.username, "email": user.email}

@user_router.post("/login")
async def login_user(request: LoginRequest):
    email = request.email
    password = request.password

    # Fetch user from the database
    user = users_collection.find_one({"email": email})

    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create access token
    access_token = create_access_token(data={"sub": user["email"]})

    return {"access_token": access_token, "token_type": "bearer"}
