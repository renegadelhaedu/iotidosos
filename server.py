from flask import *
from flask_socketio import SocketIO
from controllers.sensor_controller import SensorController

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma_chave_secreta_aqui'
socketio = SocketIO(app, cors_allowed_origins="*")


sensor_controller = SensorController()


@app.route('/alerta', methods=['GET'])
def receber_alerta():
    casa_id = request.args.get('id')
    tipo_alerta = request.args.get('tipo')

    print(f"Alerta recebido da casa {casa_id}: {tipo_alerta}")


    sensor_log = sensor_controller.processar_alerta(casa_id, tipo_alerta)


    socketio.emit('novo_alerta', {
        'casa': casa_id,
        'alerta': tipo_alerta,
        'log_id': sensor_log.id,
        'data_hora': sensor_log.data_hora.isoformat() if hasattr(sensor_log.data_hora,
                                                                 'isoformat') else sensor_log.data_hora
    })

    return jsonify({"status": "ok", "log_id": sensor_log.id}), 200


@app.route('/logs', methods=['GET'])
def obter_logs():

    casa_id = request.args.get('casa_id')


    if casa_id:
        logs = sensor_controller.obter_logs_por_casa(casa_id)
    else:
        logs = sensor_controller.obter_todos_logs()


    logs_formatados = []
    for log in logs:
        log_dict = log.to_dict()

        if hasattr(log.data_hora, 'strftime'):
            log_dict['data_hora_formatada'] = log.data_hora.strftime('%d/%m/%Y %H:%M:%S')
        else:

            try:
                from datetime import datetime
                dt = datetime.fromisoformat(str(log.data_hora).replace('Z', '+00:00'))
                log_dict['data_hora_formatada'] = dt.strftime('%d/%m/%Y %H:%M:%S')
            except (ValueError, AttributeError):
                log_dict['data_hora_formatada'] = str(log.data_hora)
        logs_formatados.append(log_dict)


    return render_template('logs.html', logs=logs_formatados, casa_id=casa_id)

@app.route('/')
def monitoramento():
    return render_template('condominio.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, allow_unsafe_werkzeug=True)