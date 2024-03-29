#!/usr/bin/env python
import os
import sys

from flask_script import Manager
from flask_migrate import MigrateCommand, upgrade

# Import settings from .env file. Must define FLASK_CONFIG
if os.path.exists(".env"):
    print("Importing environment from .env file")
    for line in open(".env"):
        var = line.strip().split("=")
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app
from app.models import Donation, Project, Contact, ContactType, MuUser

manager = Manager(create_app)
# e.g. "python manage.py --config development runserver"
manager.add_option("-c", "--config", dest="config_name", required=False)

manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)


@manager.command
def populate():
    """Populates the dev db."""
    upgrade()
    Project.populate()
    Contact.populate()
    ContactType.populate()
    MuUser.populate()
    Donation.populate()


if __name__ == "__main__":
    manager.run()
