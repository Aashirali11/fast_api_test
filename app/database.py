from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


# SQLALCHEMY_DATABASE_URL ="postgresql+psycopg://postgres:Test%40123@localhost:5432/fastapi"
SQLALCHEMY_DATABASE_URL =f"postgresql+psycopg://{settings.dbuser}:{settings.dbpass}@{settings.dbhost}:5432/{settings.dbname}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### Needed Imports for the code to work
# from app.Environment_variables import *
# import psycopg
# import time

# # Database connection retry logic
# maxattempts = 5
# retriedattempts = 1
# while retriedattempts<=maxattempts:
#     try:
#         conn = psycopg.connect(
#         host=dbhost,
#         dbname=dbname,
#         user=dbuser,   # ✅ correct parameter name and spelling
#         password=dbpass,
#         row_factory=psycopg.rows.dict_row)
#         cursor = conn.cursor()
#         print("Database Connected successfully")
#         break
#     except Exception as E:
#         print("Database Connection failed")
#         print("Error: "+str(E))
#         time.sleep(2)
    
#     finally:
#         print(f"Attempt: {retriedattempts} to connect to db server")
#         retriedattempts+=1
#     if retriedattempts >maxattempts:
#         print("Max Attempt and unable to connect to db server")

#         break
