class Pessoa:
    pi = 2.3
    def __init__(self, id_pessoa: int, nome: str, data_nascimento: str, telefone: str = None,
                 telefone_emergencia: str = None, historico_medico: str = None, numero_casa: str = None):

        self.id_pessoa = id_pessoa
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.telefone_emergencia = telefone_emergencia
        self.historico_medico = historico_medico
        self.numero_casa = numero_casa

    def to_dict(self):
        return {
            'id_pessoa': self.id_pessoa,
            'nome': self.nome,
            'data_dascimento': self.data_nascimento,
            'telefone': self.telefone,
            'telefone_emergencia': self.telefone_emergencia,
            'historico_medico': self.historico_medico,
            'numero_casa': self.numero_casa
        }
    def __repr__(self):

        return f"Pessoa(id_pessoa={self.id_pessoa}, nome='{self.nome}', numero_casa='{self.numero_casa}')"
