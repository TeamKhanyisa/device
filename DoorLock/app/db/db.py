from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from app.config.config import config

def build_engine(url: str | None) -> Engine:
    # MariaDB / MySQL via URL (e.g., mysql+pymysql://user:pass@host:3306/db)
    if url and (url.startswith("mysql://") or url.startswith("mysql+")):
        return create_engine(
            url,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_size=10,
            max_overflow=5,
            future=True,
        )

    # Fallback to SQLite for local/dev
    fallback = (Path(__file__).resolve().parent.parent / "face.db").as_posix()
    print(f"[WARN] DB_URL not set. Falling back to local SQLite: sqlite:///{fallback}")
    return create_engine(
        f"sqlite:///{fallback}",
        connect_args={"check_same_thread": False},
        future=True,
    )


engine: Engine = build_engine(config.DB_URL)


def init_schema() -> None:
    """Create table if not exists. Compatible with MySQL; tolerates SQLite."""
    ddl_mysql = """
    CREATE TABLE IF NOT EXISTS face_embeddings (
        id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
        user_id VARCHAR(64) NOT NULL DEFAULT 'anonymous',
        model_name VARCHAR(32) NOT NULL,
        img_path VARCHAR(255) NOT NULL,
        embedding MEDIUMTEXT NOT NULL,
        created_at DATETIME NOT NULL,
        step TINYINT UNSIGNED NOT NULL,
        PRIMARY KEY (id),
        INDEX idx_user_step (user_id, step),
        INDEX idx_created_at (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """

    # Try MySQL DDL first. If it fails (e.g., SQLite), fallback to simple SQLite DDL.
    try:
        with engine.begin() as conn:
            conn.execute(text(ddl_mysql))
        return
    except Exception:
        pass

    ddl_sqlite = """
    CREATE TABLE IF NOT EXISTS face_embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL DEFAULT 'anonymous',
        model_name TEXT NOT NULL,
        img_path TEXT NOT NULL,
        embedding TEXT NOT NULL,
        created_at TEXT NOT NULL,
        step INTEGER NOT NULL
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl_sqlite))


# Ensure schema available at import time
init_schema()
