from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
Session = sessionmaker()
engine = create_engine('sqlite:///database.db')
Session.configure(bind=engine)
