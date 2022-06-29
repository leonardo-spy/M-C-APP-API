from os import getenv

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from time import sleep

engine = create_engine(getenv("DATABASE_URL","mysql+pymysql://root:@localhost:3306/m_c"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    try:
        with engine.begin() as conn_local:
            Base.metadata.create_all(conn_local)
    except exc.OperationalError:
        print('Erro ao iniciar a conexão com o banco de dados, aguardando 15 segundos para o MYSQL dar o Boot up pela primeira vez...')
        sleep(15)
        with engine.begin() as conn_local:
            Base.metadata.create_all(conn_local)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()