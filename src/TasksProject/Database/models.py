from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Tasks(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    assigned_to = Column(String)
    status = Column(Boolean)
    userId = Column(Integer, ForeignKey("users.id"))
    
class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, nullable= False)
    password = Column(String, nullable=False)
    