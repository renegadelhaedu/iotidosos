from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models_db import Base, PessoaDB
from database.dao import PessoaDAO
from models.Pessoa import Pessoa
from models.log import Log

pessoa_bp = Blueprint('pessoa', __name__, url_prefix='/pessoa')


DATABASE_FILE = 'condominio.db'
DB_PATH = f"sqlite:///{DATABASE_FILE}"
engine = create_engine(DB_PATH, echo=True)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()


@pessoa_bp.route('/homepessoa')
def home_page():
    return render_template('pessoa/homepessoa.html')


@pessoa_bp.route('/')
def listar_pessoas():
    session = get_session()
    try:
        dao = PessoaDAO(session)
        pessoas = dao.obter_todas_pessoas()
        return render_template('pessoa/lista.html', pessoas=pessoas)
    finally:
        session.close()


@pessoa_bp.route('/modal/<int:id>')
def detalhes_modal_pessoa(id):

    session = get_session()
    try:
        dao = PessoaDAO(session)
        pessoa = dao.obter_pessoa_por_id(id)
        if not pessoa:
            return render_template('erro.html', mensagem="Pessoa não encontrada"), 404

        return render_template('pessoa/detalhesmodal.html', pessoa=pessoa)
    finally:
        session.close()

@pessoa_bp.route('/<int:id>')
def detalhes_pessoa(id):
    session = get_session()
    try:
        dao = PessoaDAO(session)
        pessoa = dao.obter_pessoa_por_id(id)
        if not pessoa:
            return render_template('erro.html', mensagem="Pessoa não encontrada"), 404

        return render_template('pessoa/detalhes.html', pessoa=pessoa)
    finally:
        session.close()


@pessoa_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_pessoa():
    if request.method == 'POST':
        session = get_session()
        try:
            nova_pessoa = Pessoa(
                id_pessoa=None, # id_pessoa será gerado pelo banco de dados
                nome=request.form.get('nome'),
                data_nascimento=request.form.get('data_nascimento'),
                telefone=request.form.get('telefone'),
                telefone_emergencia=request.form.get('telefone_emergencia'),
                id_telegram = request.form.get('idtelegram'),
                historico_medico=request.form.get('historico_medico'),
                numero_casa=request.form.get('numero_casa')
            )

            dao = PessoaDAO(session)
            dao.salvar_pessoa(nova_pessoa)

            return render_template('pessoa/homepessoa.html')
        finally:
            session.close()

    return render_template('pessoa/cadastropessoa.html')


@pessoa_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_pessoa(id):
    session = get_session()
    try:
        dao = PessoaDAO(session)
        pessoa_db = dao.obter_pessoa_por_id(id)
        if not pessoa_db:
            return render_template('erro.html', mensagem="Pessoa não encontrada"), 404

        if request.method == 'POST':
            dados_novos = request.form
            dao.atualizar_pessoa(pessoa_db, dados_novos)

            return jsonify({
                "status": "sucesso",
                "mensagem": "Pessoa atualizada com sucesso"
            }), 200

        return render_template('pessoa/editar.html', pessoa=pessoa_db)
    finally:
        session.close()


@pessoa_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_pessoa(id):
    session = get_session()
    try:
        dao = PessoaDAO(session)
        excluido = dao.excluir_pessoa(id)
        if excluido:
            return redirect(url_for('listar_pessoas'))
        else:
            return jsonify({
                "status": "erro",
                "mensagem": "Pessoa não encontrada"
            }), 404
    finally:
        session.close()


@pessoa_bp.route('/api/pessoas', methods=['GET'])
def api_listar_pessoas():
    """API para listar todas as pessoas (JSON)"""
    session = get_session()
    try:
        dao = PessoaDAO(session)
        pessoas = dao.obter_todas_pessoas()
        return jsonify([{
            'id_pessoa': p.id_pessoa,
            'nome': p.nome,
            'data_nascimento': p.data_nascimento,
            'telefone': p.telefone,
            'telefone_emergencia': p.telefone_emergencia,
            'historico_medico': p.historico_medico,
            'numero_casa': p.numero_casa
        } for p in pessoas])
    finally:
        session.close()


@pessoa_bp.route('/api/pessoas/<int:id>', methods=['GET'])
def api_detalhes_pessoa(id):

    session = get_session()
    try:
        dao = PessoaDAO(session)
        pessoa = dao.obter_pessoa_por_id(id)
        if not pessoa:
            return jsonify({"erro": "Pessoa não encontrada"}), 404

        return jsonify({
            'id_pessoa': pessoa.id_pessoa,
            'nome': pessoa.nome,
            'data_nascimento': pessoa.data_nascimento,
            'telefone': pessoa.telefone,
            'telefone_emergencia': pessoa.telefone_emergencia,
            'historico_medico': pessoa.historico_medico,
            'numero_casa': pessoa.numero_casa
        })
    finally:
        session.close()


@pessoa_bp.route('/por-casa/<numero_casa>')
def pessoas_por_casa(numero_casa):

    session = get_session()
    try:
        dao = PessoaDAO(session)
        pessoas = dao.obter_pessoas_por_casa(numero_casa)
        return render_template('pessoa/lista.html', pessoas=pessoas, casa_filtrada=numero_casa)
    finally:
        session.close()
