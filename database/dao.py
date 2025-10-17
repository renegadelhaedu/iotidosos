from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models_db import Base, PessoaDB, LogDB


DATABASE_FILE = 'condominio.db'
DB_PATH = f"sqlite:///{DATABASE_FILE}"

engine = create_engine(DB_PATH, echo=False)
Session = sessionmaker(bind=engine)


class PessoaDAO:
    def __init__(self, session):
        self.session = session

    def salvar_pessoa(self, pessoa):
        """Salva uma nova pessoa no banco de dados."""
        pessoa_db = PessoaDB(
            nome=pessoa.nome,
            data_nascimento=pessoa.data_nascimento,
            telefone=pessoa.telefone,
            telefone_emergencia=pessoa.telefone_emergencia,
            id_telegram=pessoa.id_telegram,
            historico_medico=pessoa.historico_medico,
            numero_casa=pessoa.numero_casa
        )
        self.session.add(pessoa_db)
        self.session.commit()
        return pessoa_db

    def obter_todas_pessoas(self):
        """Retorna todas as pessoas do banco de dados."""
        return self.session.query(PessoaDB).all()

    def obter_pessoa_por_id(self, id_pessoa):
        """Retorna uma pessoa pelo seu ID."""
        return self.session.query(PessoaDB).filter_by(id_pessoa=id_pessoa).first()

    def obter_pessoas_por_casa(self, numero_casa):
        """Retorna todas as pessoas de uma determinada casa."""
        return self.session.query(PessoaDB).filter_by(numero_casa=numero_casa).all()

    def obter_id_telegram_da_casa(self, numero_casa):
        """Retorna o id telegram da pessoa que mora em determinada casa."""
        return self.session.query(PessoaDB).filter_by(numero_casa=numero_casa).first().id_telegram


    def atualizar_pessoa(self, pessoa_db, dados_novos):
        """Atualiza os dados de uma pessoa existente no banco de dados."""
        for chave, valor in dados_novos.items():
            setattr(pessoa_db, chave, valor)
        self.session.commit()
        return pessoa_db

    def excluir_pessoa(self, id_pessoa):
        """Exclui uma pessoa do banco de dados."""
        pessoa_a_excluir = self.obter_pessoa_por_id(id_pessoa)
        if pessoa_a_excluir:
            self.session.delete(pessoa_a_excluir)
            self.session.commit()
            return True
        return False


class LogDAO:
    def __init__(self, session):
        self.session = session

    def salvar_log(self, log):
        """Salva um novo log no banco de dados"""
        log_db = LogDB(
            tipo_ocorrencia=log.tipo_ocorrencia,
            numero_casa=log.numero_casa,
            descricao=log.descricao,
            horario=log.horario
        )
        self.session.add(log_db)
        self.session.commit()
        return log_db

    def obter_todos_logs(self):
        """Retorna todos os logs do banco de dados."""
        return self.session.query(LogDB).order_by(LogDB.horario.desc()).all()

    def obter_logs_por_casa(self, numero_casa):
        """Retorna todos os logs de uma determinada casa."""
        return self.session.query(LogDB).filter_by(numero_casa=numero_casa).order_by(LogDB.horario.desc()).all()

    def obter_log_por_id(self, id_log):
        """Retorna um log pelo seu ID."""
        return self.session.query(LogDB).filter_by(id_log=id_log).first()