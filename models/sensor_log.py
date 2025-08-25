from datetime import datetime


class SensorLog:
    def __init__(self, id=None, casa_id=None, tipo_alerta=None, data_hora=None):
        self.id = id
        self.casa_id = casa_id
        self.tipo_alerta = tipo_alerta
        self.data_hora = data_hora if data_hora else datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'casa_id': self.casa_id,
            'tipo_alerta': self.tipo_alerta,
            'data_hora': self.data_hora.isoformat() if isinstance(self.data_hora, datetime) else self.data_hora
        }