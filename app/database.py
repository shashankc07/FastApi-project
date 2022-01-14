from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# postgresql://<username>:<password>@<ip-address/hostname>/<database_name>  <-- DB Connection String
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}' \
                          f':{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# connecting to postgres DB
# try:
#     conn = psycopg2.connect(host='localhost', port="8080", database='FastApi DB', user='postgres',
#                             password='shashank007', cursor_factory=RealDictCursor)
#     cur = conn.cursor()
#     print("Connected to Database Successfully !!")
#
# except Exception as e:
#     print('Oops ! Connection to Database Failed !')
#     print('Error: ', e)
