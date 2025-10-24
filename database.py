import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Força encoding UTF-8 nas variáveis de ambiente
os.environ['PGCLIENTENCODING'] = 'UTF8'
os.environ['PYTHONIOENCODING'] = 'utf-8'

## Para configurar a conexão com o banco de dados

USUARIO = "romeu"
SENHA = "3006"
HOST = "localhost"
PORTA = 5432
BANCO = "postgres"

# Permite override via variável de ambiente
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    (
        f"postgresql+psycopg2://{quote_plus(USUARIO)}:{quote_plus(SENHA)}"
        f"@{HOST}:{PORTA}/{BANCO}?client_encoding=utf8"
    ),
)

## Mecanismo de conexão
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={
            "options": "-c client_encoding=UTF8 -c lc_messages=C",
        },
        pool_pre_ping=True,
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Base
Base = declarative_base()