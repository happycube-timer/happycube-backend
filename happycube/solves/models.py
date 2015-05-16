import datetime

from happycube.database import db, Model, relationship


class Solve(Model):

    __tablename__ = 'solves'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='solves')

    scramble = db.Column(db.String(120), nullable=False)
    ellapsed_time = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Solve({ellapsed_time!r})>'.format(ellapsed_time=self.ellapsed_time)
