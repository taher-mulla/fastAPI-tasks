from datetime import timezone, datetime, timedelta
import Database.models as m
from sqlalchemy.orm import Session
from Database.database import engine, session_local
from fastapi import FastAPI, Depends, HTTPException, status, Query, Path, APIRouter
from pydantic import BaseModel, Field
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt

route = APIRouter(prefix="/auth")

SECRET_KEY = "taher"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class User_Modle(BaseModel):
    userid: str = Field(..., min_length=3)
    password: str = Field(..., min_length=3)
    
    model_config= {
        "json_schema_extra": {
            "examples": [
                {
                    "userid": "taher.mulla@gmail.com",
                    "password": "Password"
                }
            ]
        }
    }

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
db_connection_dependancy = Annotated[Session, Depends(get_db)]

@route.get("/health")
def null_func():
    return 

@route.get("/get_users")
def get_users(db: db_connection_dependancy):
    return db.query(m.Users).all() 

@route.put("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(db: db_connection_dependancy, user: User_Modle):
    user = m.Users(**user.model_dump())
    
    db.add(user)
    db.commit()
    
def create_token(username: str, duration: timedelta):
    expires = datetime.now(timezone.utc)
    data = {"username": username}
    token = jwt.encode(data, algorithm=ALGORITHM, key=SECRET_KEY)  
    print(token)
    return token

def create_access_token(username: str, expires_delta: timedelta):
    encode = {'username': username}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
@route.post("/token", response_model=Token)
async def token(db: db_connection_dependancy, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print("********* getting toekn")
    user = db.query(m.Users).filter(m.Users.userid == form_data.username).first()
    if user==None or user.password!=form_data.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    # token = create_token(form_data.username, timedelta(minutes=20))
    token = create_access_token(user.userid, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

def auth_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try: 
        print("trying to decode")
        print(token)
        details = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        print(details)
        if(details == None or details.get("username")==None):
            raise Exception("Not here")
        
        return details
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    print("********* getting current user")
    try:
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        if username is None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        print("***************"+username)
        return {'username': username}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.') 

@route.post("/auth_user")
def auth_user(user: Annotated[dict, Depends(get_current_user)]):
    print(user)
    return
    