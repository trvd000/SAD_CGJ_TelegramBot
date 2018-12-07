from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Servidores
from config import ip
import os

app = Flask(__name__)

engine = create_engine('sqlite:///servidores.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

cwd = os.getcwd()

@app.route('/<matricula>/JSON/')
def servInfoJSON(matricula):
    servidor = session.query(Servidores).filter_by(matricula = matricula).one()
    return jsonify(infoServidor=[servidor.serialize])

 
@app.route('/<matricula>/produtividade/atual/', methods=['GET', 'POST'])
def prodAtual(matricula):
    os.chdir(cwd)
    servidor = session.query(Servidores).filter_by(matricula = matricula).one()
    if (request.method == 'POST') or (request.args.get('app') == 'true'):
        if servidor.telegram_id == request.args['telegram_id']:
            os.chdir('{} - {}'.format(servidor.matricula, servidor.nome))
            list_dir = os.listdir('.')
            print(sorted(list_dir, reverse=True)[0])
            return send_file('{} - {}/{}'.format(servidor.matricula, servidor.nome, sorted(list_dir, reverse=True)[0]))#, attachment_filename=sorted(list_dir, reverse=True)[0])
        else:
            return 'Acesso negado'
    else:
        if request.args.get('telegram_id') == servidor.telegram_id:
            os.chdir('{} - {}'.format(servidor.matricula, servidor.nome))
            list_dir = os.listdir('.')
            return(sorted(list_dir, reverse=True)[0])
        else:
            return 'Acesso negado'

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host=ip, port=5000, threaded=True)