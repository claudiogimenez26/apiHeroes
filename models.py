import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Heroes(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    alignment = db.Column(db.String(255),nullable=False)	
    publisher = db.Column(db.String(255),nullable=False)	
    names = db.Column(db.String(255),nullable=False)	
    race = db.Column(db.String(255),nullable=False)	
    gender = db.Column(db.String(255),nullable=False)	
    image = db.Column(db.String(255),nullable=False)