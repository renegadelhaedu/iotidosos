from database.dao import engine, Base, Session, LogDB, PessoaDB

Base.metadata.create_all(engine)