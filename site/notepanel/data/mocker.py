﻿import os
from . import db
#from services import BoardService
from model import User, Board, Note, BoardUser, UserGroup
from sqlalchemy import func

def empty_db():
    # drop tables before recreating them with model
    db.engine.execute("DROP TABLE IF EXISTS board_user;")
    db.engine.execute("DROP TABLE IF EXISTS note;")
    db.engine.execute("DROP TABLE IF EXISTS board;")
    db.engine.execute("DROP TABLE IF EXISTS user;")

def fill_db():
    session = db.Session()
    user1 = User(name='tr', password=func.md5('123'), email='bbb')
    session.add(user1)
    user2 = User(name='ft', password=func.md5('ysance'), email='ft@yopmail.com')
    session.add(user2)
    user3 = User(name='test1', password=func.md5('ysance'), email='test1@yopmail.com')
    session.add(user3)
    session.commit()
    board1 = Board(name='Board1')
    session.add(board1)
    session.commit()
    board_user1 = BoardUser(user_id=user1.id, board_id=board1.id, user_group=UserGroup.OWNER)
    board_user2 = BoardUser(user_id=user2.id, board_id=board1.id, user_group=UserGroup.OWNER)  
    session.add(board_user1)
    session.add(board_user2)    
    session.commit()

'''
class BoardPages:
	HOME = 1
	TODO = 2
	FEATUREREQUEST = 3
	WALLOFFAME = 4
	ABOUTUS = 5
	HELP = 6
	pages = {HOME: 'TODO.nt'}
	

#load site pages as boards from files
def load_site_boards(path):
	#for file in os.listdir(path):
	for id in BoardPages.pages:
		file_path = os.path.join(path, BoardPages.pages[id])
		file = open(file_path, "r")
		import_content = file.read()
		board = BoardService().import_board(id, import_content)
'''
