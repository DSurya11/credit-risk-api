from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

db_user = os.getenv("MYSQLUSER")
db_password = os.getenv("MYSQLPASSWORD")
db_host = os.getenv("MYSQLHOST")
db_port = os.getenv("MYSQLPORT")
db_name = os.getenv("MYSQLDATABASE")

# Validate that all required database environment variables are set
_required = {
    "MYSQLUSER": db_user,
    "MYSQLPASSWORD": db_password,
    "MYSQLHOST": db_host,
    "MYSQLPORT": db_port,
    "MYSQLDATABASE": db_name,
}
_missing = [k for k, v in _required.items() if not v]
if _missing:
    raise RuntimeError(
        f"Missing required database environment variables: {', '.join(_missing)}. "
        "Set them in your .env file or in your hosting provider's environment settings."
    )

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


def create_tables():
    """Create all tables defined in models if they do not already exist."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified / created.")
