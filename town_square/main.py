from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic_extra_types.coordinate import Coordinate
from Databse_Code import *

SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db = {
    "tim": {
        "username": "tim",
        "full_name": "Tim Ruscica",
        "email": "tim@gmail.com",
        "hashed_password": "$2b$12$iXl85usmdEeVv.FLSyKCKuE6N7ypy7yzbkDM6DXg/bKYVqOSdxtYC",
        "disabled": False
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    Full_Name: str |  None = None
    disabled: bool |  None = None
    type : str 
    Business_Id : str
    Location : Coordinate
    Services_Done : list
    

class UserInDB(User):
    hashword: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def get_user(db, username: str):
    """create a UserInDB basemodel from a username"""
    user_data = get_user_data(username)
    if user_data:
        return UserInDB(**user_data)


def authenticate_user(db, username: str, password: str):
    """Returns a UserInDB basemodel from username if password is correct"""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashword):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Cretates the acces token for when you login\n
    returns an encoded jwt dict with the data and the exp date
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Gets a UserInDb object from the in_use jwt token"""
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    """Only gets the user from token if it isnt deactivated"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Cretaes the token object based on the OAuthRequestform type \n
    Only creates user if the password in the requet is valid for the user
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if user:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

print(get_password_hash("ABC"))