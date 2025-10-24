from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Veiculo(Base):
    __tablename__ = "agendamento_frota"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    placa_cm = Column(String(10), unique=True, index=True, nullable=False)
    motorista = Column(String(100))
    status = Column(String(50))
    posicao = Column(String(100))
    classe = Column(String(50))
    modelo = Column(String(100))
    placa_sr = Column(String(10))
    tipo_sr = Column(String(50))
    neokohm = Column(String(100))
    cidade = Column(String(100))
    agendamento = Column(DateTime)
    cliente = Column(String(100))