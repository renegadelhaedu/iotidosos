from flask import Blueprint, jsonify, request, render_template
from flask_socketio import SocketIO
from database.dao import LogDAO, Session

log_bp = Blueprint('log', __name__)

socketio = SocketIO()

def get_session():
    return Session()


@log_bp.route('/logs', methods=['GET'])
def obter_logs():
    numero_casa = request.args.get('casa_id')
    logs = []

    session = get_session()
    try:
        dao = LogDAO(session)
        if numero_casa:
            logs = dao.obter_logs_por_casa(numero_casa)
        else:
            logs = dao.obter_todos_logs()
        '''
        # Converte os objetos de banco de dados para dicionários para o template
        logs_formatados = []
        for log in logs:
            log_dict = log.__dict__.copy()
            log_dict['horario_formatado'] = log.horario.strftime('%d/%m/%Y %H:%M:%S')
            logs_formatados.append(log_dict)

        '''

        return render_template('logs.html', logs=logs, casa_id=numero_casa)
    finally:
        session.close()