from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


db_user = os.getenv("MYSQLUSER")
db_password = os.getenv("MYSQLPASSWORD")
db_host = os.getenv("MYSQLHOST")
db_port = os.getenv("MYSQLPORT")
db_name = os.getenv("MYSQLDATABASE")

db_url = (
    f"mysql+pymysql://{db_user}:{db_password}"
    f"@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=10,
    connect_args={"connect_timeout": 10}
)

sessionlocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
