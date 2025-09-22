from datetime import datetime
class Log:
    def __init__(self, id_log: int, tipo_ocorrencia: str, numero_casa: str, descricao: str = 'evento de sensor', horario: datetime = None):

        self.id_log = id_log
        self.tipo_ocorrencia = tipo_ocorrencia
        self.numero_casa = numero_casa
        self.descricao = descricao
        self.horario = horario if horario is not None else datetime.now()

    def formatar_horario(self):
        self.horario = self.horario.strftime('%d/%m/%Y %H:%M:%S')


    def to_dict(self):
        return {
            'id_log': self.id_log,
            'tipo_ocorrencia': self.tipo_ocorrencia,
            'numero_casa': self.numero_casa,
            'descricao': self.descricao,
            'horario': self.horario.isoformat()
        }

    def __repr__(self):

        return f"Log(id_log={self.id_log}, tipo_ocorrencia='{self.tipo_ocorrencia}', numero_casa='{self.numero_casa}', horario='{self.horario}')"
