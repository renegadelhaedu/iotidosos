from database.dao import PessoaDAO, Session
from models.log import Log

session = Session()


dao = PessoaDAO(session)
pessoas = dao.obter_todas_pessoas()

print(pessoas)