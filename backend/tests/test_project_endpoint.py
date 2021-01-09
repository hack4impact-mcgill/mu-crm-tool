import unittest
import datetime
from flask import current_app, request, jsonify
from app.models import Project
from app import create_app, db


class GetTypesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_project(self):
        project = Project(
            # id is default generated
            address="somewhere in Montreal",
            city="Montreal",
            province="Quebec",
            postalCode="H1A",
            neighbourhood="Plateau",
            year=2020,
            name="test",
            type="tester"
        )
        db.session.add(project)
        db.session.commit()

        project = Project.query.filter_by(city="Montreal").first()
        self.assertTrue(project is not None)
        self.assertTrue(project.year == 2020)
