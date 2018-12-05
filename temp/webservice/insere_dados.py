from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Servidores, Base

engine = create_engine('sqlite:///servidores.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

servidor1 = Servidores(nome='Ville Medeiros', matricula='f3011486', telegram_id='64282325', cargo='servidor')
session.add(servidor1)
session.commit()

servidor2 = Servidores(nome='Roberto Silva', matricula='f3011472', telegram_id='24852621', cargo='magistrado')
session.add(servidor2)
session.commit()

servidor3 = Servidores(nome='Lucas Sabio', matricula='f3012012', telegram_id='551376456', cargo='magistrado')
session.add(servidor3)
session.commit()

