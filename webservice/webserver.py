from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database_setup import Base, Servidores


app = Flask(__name__)

engine = create_engine('sqlite:///servidores.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/<matricula>/JSON/')
def servInfoJSON(matricula):
    servidor = session.query(Servidores).filter_by(matricula = matricula).one()
    return jsonify(infoServidor=[servidor.serialize])


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=True)