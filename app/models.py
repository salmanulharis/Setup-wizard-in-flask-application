from datetime import datetime
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	__table_args__ = {'extend_existing': True, 'schema': 'public'}
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	new_user = db.Column(db.Boolean)

	def __repr__(self):
		return f"User('{ self.username }')"

class Address(db.Model, UserMixin):
	__tablename__ = 'address'
	__table_args__ = {'extend_existing': True, 'schema': 'public'}
	id = db.Column(db.Integer, primary_key=True)
	fullname = db.Column(db.String(100))
	phone = db.Column(db.String(100))
	city = db.Column(db.String(100))
	user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

class Job(db.Model, UserMixin):
	__tablename__ = 'job'
	__table_args__ = {'extend_existing': True, 'schema': 'public'}
	id = db.Column(db.Integer, primary_key=True)
	jobname = db.Column(db.String(100))
	experience = db.Column(db.String(100))
	company = db.Column(db.String(100))
	user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

class Product(db.Model, UserMixin):
	__tablename__ = 'product'
	__table_args__ = {'extend_existing': True, 'schema': 'public'}
	id = db.Column(db.Integer, primary_key=True)
	product = db.Column(db.String(100))
	price = db.Column(db.String(100))
	validity = db.Column(db.String(100))
	description = db.Column(db.String(100))
	user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)







