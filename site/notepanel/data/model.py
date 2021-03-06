﻿from sqlalchemy import Table, Column, DateTime, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from db import Entity

class BoardPages:
	HOME = 1
	TODO = 2
	FEATUREREQUEST = 3
	WALLOFFAME = 4
	ABOUTUS = 5
	HELP = 6
	pages = {HOME: 'TODO.nt'}

class UserGroup:
    OWNER = 1 # creator of the board : allowed to modify the board, invite people, remove (?), export (?)
    ADMIN = 2 # allowed to modify and invite people
    CONTRIBUTOR = 3 # allowed to modify the board
    VIEWER = 4 # allowed to view the board

class BoardPrivacy:
    PRIVATE = 1 # only invited people are allowed to see it
    PUBLIC = 2 # all users (even not registered one's) are allowed to view it

class BoardOptions:
    NONE = 0
    ADDNOTE = 1
    ZOOMABLE = 2
    COLORABLE = 4
    RESIZABLE = 8
    ALL = ADDNOTE | ZOOMABLE | COLORABLE | RESIZABLE

class NoteOptions:
    NONE = 0
    REMOVABLE = 1
    MOVABLE = 2
    RESISZEABLE = 4 
    EDITABLE = 8
    COLORABLE = 16
    ALL = REMOVABLE | MOVABLE | RESISZEABLE | EDITABLE | COLORABLE # default mask
    
   
def from_export(object, dic):
    for k in dic.keys():
        prop = getattr(object, k)
        if type(dic[k]) != list:
            setattr(object, k, dic[k])

class User(Entity):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    name = Column(String(50))
    password = Column(String(32))
    last_seen_date = Column(DateTime, default=func.now())
    creation_date = Column(DateTime, default=func.now())
    edition_date = Column(DateTime, default=func.now())
    boards = relationship("Board", secondary="board_user", backref="users")
    user_group = UserGroup.VIEWER # not mapped because only used in a board context

    def __hash__(self):
        return self.id
    
    def __str__(self):
     return '************************************************ %s | %s | %s ' % (self.id, self.name, self.user_group)

    def to_dic(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "email": self.email, 
            "group": self.user_group
        }
    
    def to_export(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "email": self.email, 
            "user_group": self.user_group
        }
    
    def from_export(self, dic):
        return from_export(self, dic)
    

class Board(Entity):
    __tablename__ = "board"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    width = Column(Integer, default=2000)
    height = Column(Integer, default=2000)
    privacy = Column(Integer, default=BoardPrivacy.PRIVATE)
    color = Column(String(7))
    default_options = Column(Integer, default=BoardOptions.NONE)
    contributor_options = Column(Integer, default=BoardOptions.ADDNOTE)
    admin_options = Column(Integer, default=BoardOptions.ALL)
    owner_options = Column(Integer, default=BoardOptions.ALL)        
    comments = Column(String(500))
    creation_date = Column(DateTime, default=func.now())
    edition_date = Column(DateTime, default=func.now())
    notes = relationship("Note", backref="board")
        
    def __hash__(self):
        return self.id

    def to_dic(self):
        return {
            "id": self.id, 
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "privacy": self.privacy,
            "color": self.color,
            "default_options": self.default_options,
            "contributor_options": self.contributor_options,
            "admin_options": self.admin_options,
            "owner_options": self.owner_options,
            "comments": self.comments
        }
    
    def to_export(self):
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "privacy": self.privacy,
            "color": self.color,
            "default_options": self.default_options,
            "contributor_options": self.contributor_options,
            "admin_options": self.admin_options,
            "owner_options": self.owner_options,
            "comments": self.comments
        }
    
    def from_export(self, dic):
        return from_export(self, dic)

class BoardUser(Entity):
    __tablename__ = "board_user"
    board_id = Column(Integer, ForeignKey("board.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user_group = Column(Integer , default=UserGroup.VIEWER)
    creation_date = Column(DateTime, default=func.now())
    

class Note(Entity):
    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    board_id = Column(Integer, ForeignKey("board.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    value = Column(String(1000))
    width = Column(Integer)
    height = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer) # z-position of the note compared to the other (highest on the top)
    #color = Column(String(6))
    default_options = Column(Integer, default=NoteOptions.ALL)
    owner_options = Column(Integer, default=NoteOptions.ALL)
    admin_options = Column(Integer, default=NoteOptions.ALL)
    contributor_options = Column(Integer, default=NoteOptions.ALL)
    template = Column(String(20))
    lock = Column(Integer, default=UserGroup.CONTRIBUTOR)
    creation_date = Column(DateTime, default=func.now())
    edition_date = Column(DateTime, default=func.now())

    def __hash__(self):
        return self.id

    def to_dic(self):
        return {
            "id": self.id,
            #"board_id": self.board_id,
            "creator": self.user_id,
            "value": self.value,
            "width": self.width,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            #"color": self.color,
            "template": self.template,
            "default_options": self.default_options,
            "admin_options": self.admin_options,
            "owner_options": self.owner_options,
            "contributor_options": self.contributor_options
        }
    
    def to_export(self):
        return {
            "value": self.value,
            "width": self.width,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            #"color": self.color,
            "template": self.template,
            "default_options": self.default_options,
            "admin_options": self.admin_options,
            "owner_options": self.owner_options,
            "contributor_options": self.contributor_options
        }
    
    def from_export(self, dic):
        return from_export(self, dic)
    

