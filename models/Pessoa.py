class Pessoa:
    def __init__(self, nome, data_nascimento, numero_casa):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.numero_casa = numero_casa
        self.numero_casa = numero_casa

    def to_dict(self):
        return {
            'nome': self.nome,
            'numero_casa': self.numero_casa,
            'data_nascimento': self.data_nascimento

        }
