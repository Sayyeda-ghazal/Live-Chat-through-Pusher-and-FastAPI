from sqlalchemy import Column, String, DateTime, func, INTEGER, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Messages(Base):
    __tablename__ = "messages"

    id = Column(INTEGER, primary_key=True)
    username = Column(String, ForeignKey('users.username'), nullable=False)
    content = Column(String, index= True)
    send_at = Column(DateTime, default= func.now())

    user = relationship('Users', backref='messages')


class Users(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True)
    username = Column(String, unique= True, nullable= False)
