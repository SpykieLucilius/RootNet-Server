from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./smartpot.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_connection, _):
    cur = dbapi_connection.cursor()
    cur.execute("PRAGMA journal_mode=WAL")
    cur.execute("PRAGMA foreign_keys=ON")
    cur.close()


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
