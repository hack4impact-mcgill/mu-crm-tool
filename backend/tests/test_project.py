import json
import unittest
import uuid
from flask import current_app
from app import create_app, db
from app.models import Project, Contact, ContactType


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
            is_completed=True,
        )
        db.session.add(p)
        db.session.commit()

        # update a project with empty argumets
        response = self.client.put(
            "/project/{}".format(p_id),
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
            "is_completed": True,
        }
        response = self.client.put(
            "/project/{}".format(p_id),
            content_type="application/json",
            data=json.dumps(update_obj),
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertDictContainsSubset(update_obj, json_response)

        # update a project that does not exist
        response = self.client.put(
            "/project/{}".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps(update_obj),
        )
        self.assertEqual(response.status_code, 404)

    def test_get_all_types(self):
        test_list = ["dummy type", "dummy type 2"]
        p1 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood="dummy neighbourhood",
            year=2020,
            name="dummy name",
            type=test_list[0],
            contacts=[],
            is_completed=False,
        )
        p2 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood="dummy neighbourhood",
            year=2020,
            name="dummy name",
            type=test_list[1],
            contacts=[],
            is_completed=False,
        )
        db.session.add_all([p1, p2])
        db.session.commit()

        response = self.client.get("/project/types")
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response, test_list)

    def test_get_all_boroughs(self):
        test_list = ["borough1", "borough2"]
        p1 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood=test_list[0],
            year=2020,
            name="dummy name",
            type="dummy type",
            contacts=[],
            is_completed=False,
        )
        p2 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood=test_list[1],
            year=2020,
            name="dummy name",
            type="dummy type",
            contacts=[],
            is_completed=False,
        )
        db.session.add_all([p1, p2])
        db.session.commit()

        response = self.client.get("/project/boroughs")
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response, test_list)

    def test_get_specific_type(self):
        test_list = ["dummy type", "dummy type 2"]
        p1 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood="dummy neighbourhood",
            year=2020,
            name="dummy name",
            type=test_list[0],
            contacts=[],
            is_completed=False,
        )
        p2 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood="dummy neighbourhood",
            year=2020,
            name="dummy name",
            type=test_list[1],
            contacts=[],
            is_completed=False,
        )
        p3 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood="dummy neighbourhood",
            year=2020,
            name="dummy name",
            type=test_list[0],
            contacts=[],
            is_completed=False,
        )
        db.session.add_all([p1, p2, p3])
        db.session.commit()

        tester = {
            "address": "dummy address",
            "city": "dummy city",
            "province": "dummy province",
            "postal_code": "dummy postal_code",
            "neighbourhood": "dummy neighbourhood",
            "year": 2020,
            "name": "dummy name",
            "type": test_list[1],
            "contacts": [],
            "is_completed": False,
        }
        # test empty type param
        response = self.client.get("/project?type=")
        self.assertEqual(response.status_code, 404)

        response2 = self.client.get("/project?type={}".format(test_list[1]))
        json_response = json.loads(response2.get_data(as_text=True))
        self.assertDictContainsSubset(tester, json_response[0])

        response3 = self.client.get("/project?type={}".format(test_list[0]))
        json_response = json.loads(response3.get_data(as_text=True))
        self.assertEqual(len(json_response), 2)

    # test get endpoint by completion status
    def test_get_projects_by_completion_status(self):
        p1 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood="dummy neighbourhood",
            year=2020,
            name="dummy name",
            type="dummy type",
            contacts=[],
            is_completed=True,
        )
        p2 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood="dummy neighbourhood",
            year=2020,
            name="dummy name",
            type="dummy type2",
            contacts=[],
            is_completed=True,
        )
        p3 = Project(
            address="dummy address",
            city="dummy city",
            province="dummy province",
            postal_code="dummy postal_code",
            neighbourhood="dummy neighbourhood",
            year=2020,
            name="dummy name",
            type="dummy type2",
            contacts=[],
            is_completed=False,
        )
        db.session.add_all([p1, p2, p3])
        db.session.commit()

        tester1 = {
            "address": "dummy address",
            "city": "dummy city",
            "province": "dummy province",
            "postal_code": "dummy postal_code",
            "neighbourhood": "dummy neighbourhood",
            "year": 2020,
            "name": "dummy name",
            "type": "dummy type",
            "contacts": [],
            "is_completed": True,
        }
        tester2 = {
            "address": "dummy address",
            "city": "dummy city",
            "province": "dummy province",
            "postal_code": "dummy postal_code",
            "neighbourhood": "dummy neighbourhood",
            "year": 2020,
            "name": "dummy name",
            "type": "dummy type2",
            "contacts": [],
            "is_completed": False,
        }
        tester3 = {
            "address": "dummy address",
            "city": "dummy city",
            "province": "dummy province",
            "postal_code": "dummy postal_code",
            "neighbourhood": "dummy neighbourhood",
            "year": 2020,
            "name": "dummy name",
            "type": "dummy type2",
            "contacts": [],
            "is_completed": True,
        }
        # testing missing param
        response = self.client.get("/project?is-completed=")
        self.assertEqual(response.status_code, 404)

        # testing only get by completion status
        response2 = self.client.get("/project?is-completed={}".format(True))
        json_response2 = json.loads(response2.get_data(as_text=True))
        self.assertEqual(len(json_response2), 2)
        self.assertDictContainsSubset(tester1, json_response2[0])

        response3 = self.client.get("/project?is-completed={}".format(False))
        json_response3 = json.loads(response3.get_data(as_text=True))
        self.assertEqual(len(json_response3), 1)
        self.assertDictContainsSubset(tester2, json_response3[0])

        # testing get by completion status with type filtering
        response4 = self.client.get("/project?is-completed=True&type=dummy type2")
        json_response4 = json.loads(response4.get_data(as_text=True))
        self.assertEqual(len(json_response4), 1)
        self.assertDictContainsSubset(tester3, json_response4[0])

    # test get_all_projects endpoint

    def test_get_all_projects(self):
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
            is_completed=False,
        )

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
            is_completed=False,
        )
        db.session.add_all([p, p2])
        db.session.commit()

        # get all projects
        response = self.client.get("/project?")
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]["address"], "dummy address")
        self.assertEqual(json_data[1]["year"], 2020)

    def test_get_project_by_id(self):
        p_id = uuid.uuid4()

        # get a project with an id that does not exist
        response = self.client.get("/project/{}".format(p_id))
        self.assertEqual(response.status_code, 404)

        c_id = uuid.uuid4()
        c = Contact(
            id=c_id,
            name="dummy name",
            email="dummy email",
            cellphone="dummy cellphone",
            role="dummy role",
            organization="dummy organization",
            neighbourhood="dummy neighbourhood",
        )
        ct_id = uuid.uuid4()
        ct = ContactType(
            id=ct_id,
            hex_colour="#fffffff",
            type="dummy type",
            description="dummy description",
            contacts=[c],
        )
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
            contacts=[c],
            is_completed=False,
        )
        db.session.add(p)
        db.session.commit()

        # get a project with an id that exists
        response = self.client.get("/project/{}".format(p_id))
        json_response = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["id"], str(p_id))

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
                "is_completed": True,
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
                "is_completed": False,
            },
        )

        empty_response = self.client.post(
            "/project",
            json={
                "address": "",
                "city": "",
                "province": "",
                "postal_code": "",
                "neighbourhood": "",
                "year": None,
                "name": "",
                "type": "",
                "is_completed": False,
            },
        )

        # test posted correctly
        self.assertEqual(empty_response.status_code, 400)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_get_contacts_by_project(self):
        p_id = uuid.uuid4()

        # get contacts by project that does not exist
        response = self.client.get("/project/{}/contacts".format(p_id))
        self.assertEqual(response.status_code, 404)

        c0_id = uuid.uuid4()
        c0 = Contact(
            id=c0_id,
            name="dummy name",
            email="dummy email",
            cellphone="dummy cellphone",
            role="dummy role",
            organization="dummy organization",
            neighbourhood="dummy neighbourhood",
        )
        c1_id = uuid.uuid4()
        c1 = Contact(
            id=c1_id,
            name="dummy name",
            email="dummy email",
            cellphone="dummy cellphone",
            role="dummy role",
            organization="dummy organization",
            neighbourhood="dummy neighbourhood",
        )
        ct_id = uuid.uuid4()
        ct = ContactType(
            id=ct_id,
            hex_colour="#fffffff",
            type="dummy type",
            description="dummy description",
            contacts=[c0, c1],
        )
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
            contacts=[c0, c1],
            is_completed=False,
        )
        db.session.add(p)
        db.session.commit()

        # get contacts by project that exists
        response = self.client.get("/project/{}/contacts".format(p_id))
        json_response = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 2)
        actual_ids = [json_response[0]["id"], json_response[1]["id"]]
        expected_ids = [str(c0_id), str(c1_id)]
        self.assertCountEqual(expected_ids, actual_ids)
