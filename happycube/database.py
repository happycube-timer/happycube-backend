# -*- coding: utf-8 -*-
"""Database module, including the peewee database object and DB-related
utilities.
"""
from sqlalchemy.orm import relationship
from .extensions import db

relationship = relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    # INSTANCE OPERATIONS

    def save_instance(self):
        """Save the record."""
        db.session.add(self)
        db.session.commit()
        return self


    def delete_instance(self):
        """Remove the record from the database."""
        db.session.delete(self)
        return db.session.commit()


    def update_instance(self, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()


    # MODEL OPERATIONS

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it to the database."""
        instance = cls(**kwargs)
        return instance.save_instance()


    @classmethod
    def all(cls):
        """Returns a generator containing all instances."""
        return cls.query.all()


    @classmethod
    def get(cls, id):
        """Returns an instance with the specified id.
        Returns `None` if an instance with the specified id does not exist.
        :param id: the instance id
        """
        return cls.query.get(id)


    @classmethod
    def get_all(cls, *ids):
        """Returns a list of instances with the specified ids.
        :param *ids: instance ids
        """
        return cls.query.filter(cls.id.in_(ids)).all()


    @classmethod
    def find(cls, **kwargs):
        """Returns a list of instances filtered by the
        specified key word arguments.
        :param **kwargs: filter parameters
        """
        return cls.query.filter_by(**kwargs)


    @classmethod
    def first(cls, **kwargs):
        """Returns the first instance found filtered by
        the specified key word arguments.
        :param **kwargs: filter parameters
        """
        return cls.find(**kwargs).first()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True




from rq import Queue
from redis import Redis
# Queue for processing orders
redis_connection = Redis('localhost', 6379)
queue_new_orders = Queue('new_orders', async=True, connection=redis_connection)

