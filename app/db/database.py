from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

engine = None
sessionlocal = None

base = declarative_base()

def init_db():
    global engine, sessionlocal

    if engine is None:
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

def get_db():
    if sessionlocal is None:
        init_db()

    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
