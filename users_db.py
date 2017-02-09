from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
Session = sessionmaker()
engine = create_engine('sqlite:///users.db')
Session.configure(bind=engine)
