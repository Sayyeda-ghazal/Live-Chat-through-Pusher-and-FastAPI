from sqlalchemy.orm import Session
from . import models
from model.models import Messages, Users

def create_message(db: Session, message: str, username: str):
    try:
        user = db.query(Users).filter(Users.username == username).first()
        if not user:
            user = Users(username=username)
            db.add(user)
            db.commit()
            db.refresh(user)  
        new_message = Messages(username=username, content=message)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        print(f"Message '{message}' saved by {username}")
        return new_message

    except Exception as e:
        print(f"Error saving message: {e}")
        db.rollback()


def get_all_messages(db: Session):
    return db.query(models.Messages).all()
