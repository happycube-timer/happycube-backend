# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from random import randint

from flask.ext.script import Manager, Shell, Server

from happycube.app import create_app
from happycube.settings import DevConfig, ProdConfig
from happycube.database import db

from happycube.users.models import User
from happycube.solves.models import Solve


if os.environ.get("happycube_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {
        'app': app,
        'db': db,
        'User': User
    }

@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

@manager.command
def reset_db():
    print("____________________________________")
    # db.connect()

    # tables = [Asset, Pair, Order, User, Balance, Book, Trade]

    print("dropping existing tables")
    # db.drop_tables(tables, safe=True)
    db.session.commit()
    db.drop_all()

    print("creating tables")
    # db.create_tables(tables)
    db.create_all()

    print("adding users")
    alice = User.create(name='alice', password='papapa22')
    bob = User.create(name='bob', password='papapa22')
    # # print(alice)
    # # print(bob)

    print("adding solves")
    Solve.create(user=alice, scramble='FRURUF', ellapsed_time=50000)
    Solve.create(user=alice, scramble='FRURUF', ellapsed_time=34000)


    # db.close()


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
