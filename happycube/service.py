# -*- coding: utf-8 -*-
"""
    happycube.services
    ~~~~~~~~~~~~~
    core module
"""


from happycube.database import db


class BaseService(object):
    """A :class:`Service` instance encapsulates common SQLAlchemy model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None

    def _isinstance(self, model, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.
        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        rv = isinstance(model, self.__model__)
        if not rv and raise_error:
            raise ValueError('{} is not of type {}'.format(model, self.__model__))
        return rv

    # def _preprocess_params(self, kwargs):
    #     """Returns a preprocessed dictionary of parameters. Used by default
    #     before creating a new instance or updating an existing instance.
    #     :param kwargs: a dictionary of parameters
    #     """
    #     kwargs.pop('csrf_token', None)
    #     return kwargs

    def save(self, instance):
        """Commits the instance to the database and returns the instance
        :param instance: the instance to save
        """
        self._isinstance(instance)
        return instance.save()

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return self.__model__.all()

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.
        :param id: the instance id
        """
        return self.__model__.get(id)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.
        :param *ids: instance ids
        """
        return self.__model__.get_all(*ids)

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.
        :param **kwargs: filter parameters
        """
        return self.__model__.find(**kwargs)

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.
        :param **kwargs: filter parameters
        """
        return self.__model__.first(**kwargs)

    # def get_or_404(self, id):
    #     """Returns an instance of the service's model with the specified id or
    #     raises an 404 error if an instance with the specified id does not exist.
    #     :param id: the instance id
    #     """
    #     return self.__model__.query.get_or_404(id)

    # def new(self, **kwargs):
    #     """Returns a new, unsaved instance of the service's model class.
    #     :param **kwargs: instance parameters
    #     """
    #     return self.__model__(**kwargs)

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.
        :param **kwargs: instance parameters
        """
        return self.__model__.create(**kwargs)

    def update(self, instance, **kwargs):
        """Returns an updated instance of the service's model class.
        :param instance: the instance to update
        :param **kwargs: update parameters
        """
        self._isinstance(instance)
        return instance.update(**kwargs)

    def delete(self, instance):
        """Immediately deletes the specified instance.
        :param instance: the instance instance to delete
        """
        self._isinstance(instance)
        return instance.delete()
