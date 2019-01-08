from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Servidores, Base, Subordinados

engine = create_engine('sqlite:///servidores.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

subordinado1 = Subordinados(nome='Luquinhas', matricula='f3011548', magistrado='f3012000', cargo='magistrado')
session.add(subordinado1)
session.commit()


