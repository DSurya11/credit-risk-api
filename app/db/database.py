from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import logging

# Load .env for local development only; override=False ensures
# hosting-provider env vars (Render, Railway, etc.) take precedence.
load_dotenv(override=False)

logger = logging.getLogger(__name__)

# Render provides DATABASE_URL when a PostgreSQL database is linked.
# Fall back to building a MySQL URL from individual env vars for local dev.
db_url = os.getenv("DATABASE_URL")

if db_url:
    # Render gives postgres:// but SQLAlchemy needs postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    logger.info("Using DATABASE_URL for database connection")
else:
    # Fallback: build URL from individual environment variables
    db_user = os.getenv("MYSQLUSER")
    db_password = os.getenv("MYSQLPASSWORD")
    db_host = os.getenv("MYSQLHOST")
    db_port = os.getenv("MYSQLPORT")
    db_name = os.getenv("MYSQLDATABASE")

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
            f"Missing database config: set DATABASE_URL or all of "
            f"{', '.join(_missing)} in your environment."
        )

    db_url = (
        f"mysql+pymysql://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )
    logger.info("Using MySQL connection at %s:%s/%s", db_host, db_port, db_name)

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=10,
)

sessionlocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
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

