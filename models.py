__author__ = 'devndraghimire'
import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('robot.db') #Datbase Definition

class User(UserMixin,Model):   #USERMIXIN TO USE authenticate,active,anonymous,get_id()method
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False) #For scaling

    class Meta:
        database = DATABASE
        order_by =('-joined_at',)

    @classmethod    #if we do not have classmethod we have to create user instance to call createuser. cls utilize the self Class Method inside Class User model
    def create_user(cls, username,email,password,admin=False):
        try:
            cls.create(
                username=username,
                email= email,
                password= generate_password_hash(password),
                is_admin =admin
            )
        except IntegrityError:
            raise ValueError('User already exists')

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe =True)
    DATABASE.close()