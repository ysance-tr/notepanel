from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

Session = None
Entity = declarative_base()
engine = None

def configure(connection_string):
    global engine, Session
    engine_string = get_MySQL_engine_string(connection_string)
    engine = create_engine(engine_string, echo=True)
    Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    
def get_MySQL_engine_string(connection_string):
    connection_string_parts = connection_string.split(";")
    connection_elts = dict()
    for part in connection_string_parts:
        assignement_parts = part.split("=")            
        key = assignement_parts[0]
        value = assignement_parts[1]
        connection_elts[key] = value
    engine_string = "mysql://%s:%s@%s/%s" % (connection_elts['User Id'], connection_elts['Password'], connection_elts['Data Source'], connection_elts['Database'])
    return engine_string

def create_model():
    Entity.metadata.create_all(engine)

def initialize(dbname):
    engine.execute("CREATE DATABASE IF NOT EXISTS %s;" % dbname)    
    engine.execute("USE %s;" % dbname)
    # drop tables before recreating them with model
    engine.execute("DROP TABLE IF EXISTS board_user;") 
    engine.execute("DROP TABLE IF EXISTS note;") 
    engine.execute("DROP TABLE IF EXISTS board;")    
    engine.execute("DROP TABLE IF EXISTS user;") 
