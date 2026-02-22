from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "mysql+mysqlconnector://root:porsche718~1%21%40@localhost:3306/pricesenseai"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)