from sqlalchemy import Column, Integer, String
from database import Base

class Veiculo(Base):
    __tablename__ = "agendamento_frota"  # nome da tabela no banco

    id = Column(Integer, primary_key=True, index=True)
    placa_cm = Column(String, unique=True, index=True)
    placa_sr = Column(String)
    ano_cm = Column(Integer)
    ano_sr = Column(Integer)
