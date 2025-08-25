from database.dao import DatabaseHandler
from models.sensor_log import SensorLog


class SensorController:
    def __init__(self):
        self.db_handler = DatabaseHandler()

    def processar_alerta(self, casa_id, tipo_alerta):

        log_id = self.db_handler.insert_log(casa_id, tipo_alerta)


        return SensorLog(id=log_id, casa_id=casa_id, tipo_alerta=tipo_alerta)

    def obter_todos_logs(self):
        logs_data = self.db_handler.get_all_logs()
        logs = []
        for log_data in logs_data:
            logs.append(SensorLog(
                id=log_data[0],
                casa_id=log_data[1],
                tipo_alerta=log_data[2],
                data_hora=log_data[3]
            ))
        return logs

    def obter_logs_por_casa(self, casa_id):
        logs_data = self.db_handler.get_logs_by_casa(casa_id)
        logs = []
        for log_data in logs_data:
            logs.append(SensorLog(
                id=log_data[0],
                casa_id=log_data[1],
                tipo_alerta=log_data[2],
                data_hora=log_data[3]
            ))
        return logs

    def obter_logs_por_tipo(self, tipo_alerta):
        logs_data = self.db_handler.get_logs_by_tipo(tipo_alerta)
        logs = []
        for log_data in logs_data:
            logs.append(SensorLog(
                id=log_data[0],
                casa_id=log_data[1],
                tipo_alerta=log_data[2],
                data_hora=log_data[3]
            ))
        return logs