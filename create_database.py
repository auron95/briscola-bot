import models
from models import Base

from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db', echo=True)

Base.metadata.create_all(engine)


