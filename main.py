from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import models

app = FastAPI(title="API Frota", version="1.0.0")

# Cria as tabelas no banco quando a aplicação iniciar
@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

# Dependência: gerencia conexão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema para receber dados do veículo
class VeiculoCreate(BaseModel):
    placa_cm: str
    motorista: Optional[str] = None
    status: Optional[str] = None
    posicao: Optional[str] = None
    classe: Optional[str] = None
    modelo: Optional[str] = None
    placa_sr: Optional[str] = None
    tipo_sr: Optional[str] = None
    neokohm: Optional[str] = None
    cidade: Optional[str] = None
    agendamento: Optional[datetime] = None
    cliente: Optional[str] = None

# Schema para atualizar dados
class VeiculoUpdate(BaseModel):
    placa_cm: Optional[str] = None
    motorista: Optional[str] = None
    status: Optional[str] = None
    posicao: Optional[str] = None
    classe: Optional[str] = None
    modelo: Optional[str] = None
    placa_sr: Optional[str] = None
    tipo_sr: Optional[str] = None
    neokohm: Optional[str] = None
    cidade: Optional[str] = None
    agendamento: Optional[datetime] = None
    cliente: Optional[str] = None

@app.get("/")
def home():
    return {
        "mensagem": "API de Gestão de Frota",
        "versao": "1.0.0",
        "endpoints": [
            "GET /frota - Listar todos os veículos",
            "GET /frota/{id} - Buscar veículo por ID",
            "POST /frota - Adicionar novo veículo",
            "PUT /frota/{id} - Atualizar veículo",
            "DELETE /frota/{id} - Deletar veículo"
        ]
    }

@app.get("/frota")
def listar_veiculos(db: Session = Depends(get_db)):
    """Lista todos os veículos cadastrados"""
    try:
        veiculos = db.query(models.Veiculo).all()
        return {
            "total": len(veiculos),
            "veiculos": veiculos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar veículos: {str(e)}")

@app.get("/frota/{veiculo_id}")
def buscar_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """Busca um veículo específico por ID"""
    veiculo = db.query(models.Veiculo).filter(models.Veiculo.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo

@app.post("/frota", status_code=201)
def adicionar_veiculo(veiculo: VeiculoCreate, db: Session = Depends(get_db)):
    """Adiciona um novo veículo"""
    try:
        novo_veiculo = models.Veiculo(**veiculo.dict())
        db.add(novo_veiculo)
        db.commit()
        db.refresh(novo_veiculo)
        return {
            "mensagem": "Veículo adicionado com sucesso!",
            "veiculo": novo_veiculo
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Placa CM já cadastrada")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao adicionar veículo: {str(e)}")

@app.put("/frota/{veiculo_id}")
def atualizar_veiculo(veiculo_id: int, veiculo_update: VeiculoUpdate, db: Session = Depends(get_db)):
    """Atualiza dados de um veículo"""
    veiculo = db.query(models.Veiculo).filter(models.Veiculo.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    
    try:
        # Atualiza apenas os campos fornecidos
        update_data = veiculo_update.dict(exclude_unset=True)
        for campo, valor in update_data.items():
            setattr(veiculo, campo, valor)
        
        db.commit()
        db.refresh(veiculo)
        return {
            "mensagem": "Veículo atualizado com sucesso!",
            "veiculo": veiculo
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Placa CM já existe")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar: {str(e)}")

@app.delete("/frota/{veiculo_id}")
def deletar_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """Deleta um veículo"""
    veiculo = db.query(models.Veiculo).filter(models.Veiculo.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    
    try:
        db.delete(veiculo)
        db.commit()
        return {"mensagem": f"Veículo {veiculo.placa_cm} deletado com sucesso!"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar: {str(e)}")