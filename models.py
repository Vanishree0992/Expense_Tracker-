from extensions import db
from flask_login import UserMixin
from datetime import date

shared_accounts = db.Table('shared_accounts',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('account_id', db.Integer, db.ForeignKey('account.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    emails = db.relationship('Transaction', backref='owner', lazy=True)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transactions = db.relationship('Transaction', backref='account', lazy=True)
    shared_with = db.relationship('User', secondary=shared_accounts, backref='shared_accounts')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    amount = db.Column(db.Float)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='USD')
    date = db.Column(db.Date, default=date.today)
    description = db.Column(db.String(255))
    recurring = db.Column(db.Boolean, default=False)
    receipt_file = db.Column(db.String(255))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
