import json
import unittest
import uuid
from flask import current_app
from app import create_app, db
from app.models import ContactType


class ContactTypeTestCase(unittest.TestCase):
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

    def test_contact_type_routes(self):
        ct_id = uuid.uuid4()
        ct = ContactType(
            id=ct_id,
            hex_colour="#ffffff",
            type="dummy type",
            description="dummy description",
        )
        db.session.add(ct)
        db.session.commit()

        # deleting a contact_type that exists
        response = self.client.delete("/contact_type/{}".format(ct_id))
        self.assertEqual(response.status_code, 200)

        # deleting a contact_type that does not exist
        response = self.client.delete("/contact_type/{}".format(ct_id))
        self.assertEqual(response.status_code, 404)
        
    def test_create_contact_type_route(self):
        # creating a contact_type with valid arguments
        valid_response = self.client.post(
            "/contact_type",
            json={
                "hex_colour": "#F0F8FF",
                "type": "dummy type",
                "description": "dummy description",
            },
        )

        # creating a contact_type with valid arguments
        valid_response2 = self.client.post(
            "/contact_type",
            json={
                "hex_colour": "#ffffff",
                "type": "new dummy type",
                "description": "new dummy description",
            },
        )

        # creating a contact_type with valid arguments
        valid_response3 = self.client.post(
            "/contact_type",
            json={
                "hex_colour": "#ffffff",
                "type": "dummy type 3",
                "description": "dummy description 3",
            },
        )

        # creating a contact_type with empty arguments
        empty_response = self.client.post(
            "/contact_type",
            json={
                "hex_colour": "",
                "type": "",
                "description": "",
            },
        )

        # checking that the tests worked
        self.assertEqual(valid_response.status_code, 200)
        self.assertEqual(valid_response2.status_code, 200)
        self.assertEqual(valid_response3.status_code, 200)
        self.assertEqual(empty_response.status_code, 400)

        returned_json = self.client.get("")
        json_data = returned_json.get_json()
        self.assertEqual(len(json_data), 3)

        # checking that the valid responses have two unique ids
        self.assertNotEqual(json_data[0]["id"], json_data[1]["id"])

        self.assertEqual(json_data[0]["type"], "dummy type")
        self.assertEqual(json_data[1]["hex_colour"], "#ffffff")
        self.assertEqual(json_data[2]["description"], "dummy description 3")