from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from bson import ObjectId
from database import db
from blog_app.users.models import User
from blog_app.users.routes import users_collection
from dotenv import load_dotenv
import os
load_dotenv()

# Secret and algorithm configuration
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')



# OAuth2 scheme for extracting the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Exception for invalid credentials
credentials_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Retrieve the current user from the database using the token's payload.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")  # Assuming 'sub' is the user's email in the token
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch user from the database by email, not by ObjectId
    user_obj = users_collection.find_one({"email": user_email})
    if not user_obj:
        raise credentials_exception

    # Convert ObjectId to str before creating the User instance
    user_obj["id"] = str(user_obj["_id"])  # Ensure you convert ObjectId to string
    return User(**user_obj)