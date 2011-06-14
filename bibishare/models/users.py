import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime

from bibishare.models import Base



class User(Base):    
    __tablename__ = 'users'
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    fullname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, )
    
    def __init__(self, username, password, fullname, email, group=None):
        self.username = username
        self.password = password

        self.fullname = fullname
        self.email = email
