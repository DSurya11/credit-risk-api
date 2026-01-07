from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

mysql_user = os.environ["MYSQLUSER"]
mysql_password = os.environ["MYSQLPASSWORD"]
mysql_host = os.environ["MYSQLHOST"]
mysql_port = os.environ["MYSQLPORT"]
mysql_db = os.environ["MYSQLDATABASE"]

db_url = (
    f"mysql+pymysql://{mysql_user}:{mysql_password}"
    f"@{mysql_host}:{mysql_port}/{mysql_db}"
)

engine = create_engine(db_url, pool_pre_ping=True)

sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
