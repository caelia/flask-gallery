#!/usr/bin/env python

from flask import Flask
from flask_sqlalchemy import sqlalchemy
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell


app = Flask(__name__)
db = SQLAlchemy(app)
manager = Manager(app)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_no = db.Column(db.String(32), unique=True)
    title = db.Column(db.String(256))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('creators.id'))

    def __repr__(self):
        return '<Item: %r - %r>' % (self.item_no, self.title)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    items = db.relationship('Item', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category: %r>' % self.name

class Creator(db.Model):
    __tablename__ = 'creators'
    id = db.Column(db.Integer, primary_key=True)
    name1 = db.Column(db.String(128))
    name2 = db.Column(db.String(256))
    display_order = db.Column(db.Integer)

    def display_name(self):
        if self.display_order == 0:
            return '%s %s' % (self.name1, self.name2)
        else:
            return '%s %s' % (self.name2, self.name1)

    def __repr__(self):
        return '<Creator: %r>' % self.display_name()

class ItemUploadForm(Form):
    item_no = StringField('Item No:')
    title = StringField('Title:', validators=[Required()])
    category = StringField('Category:')
