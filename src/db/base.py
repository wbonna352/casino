from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

config = dict(
  host="localhost",
  port="5432",
  database="casino",
  user="casino",
  password="casino"
)

engine = create_engine(
    f"""postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"""
)

session = scoped_session(
    sessionmaker(
        autoflush=False,
        autocommit=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = session.query_property()
