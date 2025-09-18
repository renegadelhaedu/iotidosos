from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PessoaDB(Base):

    __tablename__ = 'pessoas'

    id_pessoa = Column(Integer, primary_key=True)
    nome = Column(String)
    data_nascimento = Column(String)
    telefone = Column(String)
    telefone_emergencia = Column(String)
    historico_medico = Column(String)
    numero_casa = Column(String)

    def __repr__(self):
        return f"<PessoaDB(nome='{self.nome}', numero_casa='{self.numero_casa}')>"

class LogDB(Base):
    __tablename__ = 'logs'

    id_log = Column(Integer, primary_key=True)
    tipo_ocorrencia = Column(String)
    numero_casa = Column(String)
    descricao = Column(String)
    horario = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<LogDB(tipo_ocorrencia='{self.tipo_ocorrencia}', numero_casa='{self.numero_casa}', horario='{self.horario}')>"
