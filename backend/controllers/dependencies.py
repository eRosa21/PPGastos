#from src.infra.entities.models import db
from sqlalchemy.orm import sessionmaker 


def catch_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session() 
        yield session
    finally:
        db.close()