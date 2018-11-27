from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Servidores, Base

engine = create_engine('sqlite:///servidores.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

servidor1 = Servidores(nome='Ville Medeiros', matricula='f3011486', telegram_id=)