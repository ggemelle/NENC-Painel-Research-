from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco
DATABASE_URL = "postgresql://postgres:admin@localhost/pesquisa_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Modelos do banco
class Participante(Base):
    __tablename__ = "participantes"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)

class Resposta(Base):
    __tablename__ = "respostas"
    id = Column(Integer, primary_key=True)
    participante_id = Column(Integer, ForeignKey("participantes.id"))
    pesquisa_id = Column(Integer, nullable=False)
    resposta = Column(Text, nullable=False)

# Criar tabelas
Base.metadata.create_all(engine)
