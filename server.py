import eventlet
eventlet.monkey_patch()

import tocarsom
from controllers.buzzer import apitar

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from controllers.pessoa_bp import pessoa_bp
from controllers.log_bp import log_bp
from database.dao import engine, Base, PessoaDAO, Session, LogDAO
from models.log import Log
from controllers.telegram import send_telegram_message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LJlhr3324DH1'
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(pessoa_bp)
app.register_blueprint(log_bp)


def executar_audio():
    #apitar()
    tocarsom.tocar_som('lulu.mp3')


@app.route('/')
def monitoramento():
    session = Session()
    try:
        dao = PessoaDAO(session)
        pessoas = dao.obter_todas_pessoas()
        return render_template('condominio.html', pessoas=pessoas)
    finally:
        session.close()


@app.route('/alerta', methods=['GET'])
def receber_alerta():
    session = Session()
    numero_casa = request.args.get('id')
    tipo_alerta = request.args.get('tipo')

    id_telegram = PessoaDAO(session).obter_id_telegram_da_casa(numero_casa)
    resultado_telegram = send_telegram_message(tipo_alerta, numero_casa, id_telegram)

    #eventlet.spawn_n(executar_audio)

    descricao = f"Alerta recebido da casa {numero_casa}: {tipo_alerta}"


    try:

        novo_log = Log(
            id_log=None,
            tipo_ocorrencia=tipo_alerta,
            numero_casa=numero_casa,
            descricao=descricao
        )
        dao = LogDAO(session)
        log_salvo = dao.salvar_log(novo_log)


        socketio.emit('novo_alerta', {
            'casa': numero_casa,
            'alerta': tipo_alerta,
            'log_id': log_salvo.id_log,
            'data_hora': log_salvo.horario.isoformat()
        })



        session.close()
        return jsonify({
            "status": "Recebido",
            "log_id": log_salvo.id_log,
            "telegram": resultado_telegram
        }), 200

    except Exception as e:
        print("Erro no alerta:", e)
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    #NAO APAGUE
    #gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 server:app
    socketio.run(app,
                 host='0.0.0.0',
                 port=5000,
                 debug=True,
                 allow_unsafe_werkzeug=True)
