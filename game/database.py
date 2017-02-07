from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
Session = sessionmaker()
engine = create_engine('sqlite:///database.db', echo=True)
Session.configure(bind=engine)
