import json
import unittest
import uuid
from flask import current_app
from app import create_app, db
from app.models import Project


class ProjectTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_project_routes(self):
        p_id = uuid.uuid4()
        p = Project(
            id=p_id,
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood="dummy neighbourhood",
            year=2020,
            name="dummy name",
            type="dummy type",
            contacts=[],
        )
        db.session.add(p)
        db.session.commit()

        # update a project with empty arguments
        response = self.client.put(
            "/project/{}/update".format(p_id),
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, 400)

        # update a project with valid arguments
        update_obj = {
            "address": "new dummy address",
            "city": "new dummy city",
            "province": "new dummy province",
            "postal_code": "new dummy postal_code",
            "neighbourhood": "new dummy neighbourhood",
            "year": 2021,
            "name": "new dummy name",
            "type": "new dummy type",
        }
        response = self.client.put(
            "/project/{}/update".format(p_id),
            content_type="application/json",
            data=json.dumps(update_obj),
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertDictContainsSubset(update_obj, json_response)

        # update a project that does not exist
        response = self.client.put(
            "/project/{}/update".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps(update_obj),
        )
        self.assertEqual(response.status_code, 404)
