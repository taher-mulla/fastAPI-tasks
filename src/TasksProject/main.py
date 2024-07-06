import Database.models as m
from sqlalchemy.orm import Session
from Database.database import engine, session_local
from fastapi import FastAPI, Depends, HTTPException, status, Query, Path, APIRouter
from pydantic import BaseModel, Field
from typing import Annotated
import Auth.auth
import Home.home as home


app = FastAPI()


m.Base.metadata.create_all(bind=engine)

app.include_router(Auth.auth.route)
app.include_router(home.route)