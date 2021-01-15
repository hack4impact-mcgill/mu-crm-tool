import json
import unittest
import uuid
from flask import current_app, request
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

    def test_update_project(self):
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

        # update a project with empty argumets
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

    # test get_projects endpoint
    def test_get_project(self):
        # pre-populate database
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

        p2_id = uuid.uuid4()
        p2 = Project(
            id=p2_id,
            address="dummy address 2",
            city="dummy city 2",
            province="dummy province 2",
            postal_code="dummy postal_code 2",
            neighbourhood="dummy neighbourhood 2",
            year=2020,
            name="dummy name 2",
            type="dummy type 2",
            contacts=[],
        )
        db.session.add(p2)
        db.session.commit()

        # get all projects
        response = self.client.get("/project")
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]["address"], "dummy address")
        self.assertEqual(json_data[1]["year"], 2020)

    def test_create_project(self):
        response = self.client.post(
            "/project",
            json={
                "address": "dummy address 2",
                "city": "dummy city 2",
                "province": "dummy province 2",
                "postal_code": "dummy postal_code 2",
                "neighbourhood": "dummy neighbourhood 2",
                "year": 2020,
                "name": "dummy name 2",
                "type": "dummy type 2",
                "contacts": [],
            },
        )
        response2 = self.client.post(
            "/project",
            json={
                "address": "dummy address",
                "city": "dummy city",
                "province": "dummy province",
                "postal_code": "dummy postal_code",
                "neighbourhood": "dummy neighbourhood",
                "year": 2020,
                "name": "dummy name",
                "type": "dummy type",
                "contacts": [],
            },
        )

        empty_response = self.client.post("/project", json={"address": ""})

        # test posted correctly
        self.assertEqual(empty_response.status_code, 400)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

        returned_json = self.client.get("/project")
        json_data = returned_json.get_json()
        self.assertEqual(len(json_data), 2)

        # test two unique uuid genearted correctly
        self.assertNotEqual(json_data[0]["id"], json_data[1]["id"])
