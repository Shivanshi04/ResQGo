from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'user', 'volunteer', 'admin'
    region = db.Column(db.String(50), nullable=False)
    family_contact = db.Column(db.String(20), nullable=True)

class EmergencyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    emergency_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    region = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Pending') # 'Pending', 'Resolved'

    user = db.relationship('User', backref=db.backref('emergencies', lazy=True))
