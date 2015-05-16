import datetime

from happycube.database import db, Model, relationship
from happycube.extensions import bcrypt


class User(Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, name, password=None, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    # @property
    # def full_name(self):
    #     return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({name!r})>'.format(name=self.name)
