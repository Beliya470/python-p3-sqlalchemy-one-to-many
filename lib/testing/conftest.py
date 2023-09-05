#!/usr/bin/env python3

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

package_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[0:-1])
db_dir = os.path.join(package_dir, 'one_to_many.db')
SQLITE_URL = ''.join(['sqlite:///', db_dir])

# Initialize the database engine and create tables
engine = create_engine(SQLITE_URL)
Base.metadata.create_all(engine)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
