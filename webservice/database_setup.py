import sys
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Servidores(Base):
    __tablename__ = 'servidores'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80), nullable=False)
    telegram_id = Column(Integer, nullable=False)
    matricula = Column(String(15), nullable=False)
    cargo = Column(String(20), nullable=False)

    @property
    def serialize(self):
        return{
            'nome' : self.nome,
            'id' : self.telegram_id,
            'matricula' : self.matricula,
            'cargo' : self.cargo,
        }

engine = create_engine('sqlite:///servidores.db')
Base.metadata.create_all(engine)