import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Força encoding UTF-8
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

os.environ['PGCLIENTENCODING'] = 'UTF8'
os.environ['PYTHONIOENCODING'] = 'utf-8'

## Configuração do banco
USUARIO = "romeu"
SENHA = "3006"
HOST = "localhost"
PORTA = 5432
BANCO = "postgres"

# String de conexão com encoding explícito
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{quote_plus(USUARIO)}:{quote_plus(SENHA)}@{HOST}:{PORTA}/{BANCO}"
)

## Mecanismo de conexão
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "client_encoding": "utf8",
    },
    pool_pre_ping=True,
    echo=False,  # Mude para True se quiser ver os SQL sendo executados
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Base
Base = declarative_base()