from flask import Blueprint, jsonify, request, render_template
from flask_socketio import SocketIO
from database.dao import LogDAO, Session
from models.log import Log

# Criação do Blueprint para as rotas de log
log_bp = Blueprint('log', __name__)

# Instância do SocketIO para emitir eventos
socketio = SocketIO()

def get_session():
    """Retorna uma nova sessão de banco de dados."""
    return Session()


@log_bp.route('/logs', methods=['GET'])
def obter_logs():
    """Exibe os logs de ocorrências em uma página web."""
    numero_casa = request.args.get('casa_id')
    logs = []

    session = get_session()
    try:
        dao = LogDAO(session)
        if numero_casa:
            # Busca logs de uma casa específica
            logs = dao.obter_logs_por_casa(numero_casa)
        else:
            # Busca todos os logs
            logs = dao.obter_todos_logs()

        # Converte os objetos de banco de dados para dicionários para o template
        logs_formatados = []
        for log in logs:
            log_dict = log.__dict__.copy()
            log_dict['horario_formatado'] = log.horario.strftime('%d/%m/%Y %H:%M:%S')
            logs_formatados.append(log_dict)

        return render_template('logs.html', logs=logs_formatados, casa_id=numero_casa)
    finally:
        session.close()