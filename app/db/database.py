from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import logging
import ssl as _ssl

# Load .env for local development only; override=False ensures
# hosting-provider env vars (Render, Railway, etc.) take precedence.
load_dotenv(override=False)

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

logger.info(
    "Connecting to MySQL at %s:%s/%s as %s",
    db_host, db_port, db_name, db_user,
)

db_url = (
    f"mysql+pymysql://{db_user}:{db_password}"
    f"@{db_host}:{db_port}/{db_name}"
)

# Build connect_args — Railway public endpoints may require SSL
connect_args: dict = {"connect_timeout": 30}

# Use SSL when connecting to a remote host (not localhost/127.0.0.1)
if db_host not in ("localhost", "127.0.0.1", "::1"):
    ssl_ctx = _ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = _ssl.CERT_NONE
    # pymysql uses 'ssl_context' for SSLContext objects
    connect_args["ssl_context"] = ssl_ctx
    logger.info("SSL enabled for remote MySQL connection")

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_recycle=1800,
    pool_size=5,
    max_overflow=10,
    connect_args=connect_args,
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
