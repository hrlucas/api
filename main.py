from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

app = FastAPI()

# Cria a tabela no banco quando a aplicação iniciar
@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)

# Dependência: cria e fecha conexão com o banco automaticamente
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"mensagem": "Minha primeira API"}

@app.get("/frota")
def listar_veiculos(db: Session = Depends(get_db)):
    veiculos = db.query(models.Veiculo).all()
    return veiculos
