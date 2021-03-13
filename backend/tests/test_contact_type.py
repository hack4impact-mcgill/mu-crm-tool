import json
import unittest
import uuid
from flask import current_app
from app import create_app, db
from app.models import ContactType, Contact


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

    def test_delete_a_contact_type(self):
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
                "hex_colour": "#f0f8ff",
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

        types = ContactType.query.all()
        first_type = types[0]
        second_type = types[1]
        third_type = types[2]

        # checking that the valid responses have two unique ids
        self.assertNotEqual(first_type.id, second_type.id)

        self.assertEqual(first_type.type, "dummy type")
        self.assertEqual(second_type.hex_colour, "#ffffff")
        self.assertEqual(third_type.description, "dummy description 3")

    # testing get all contact types endpoint
    def test_get_all_contact_types_route(self):
        ct_id1 = uuid.uuid4()
        ct_1 = ContactType(
            id=ct_id1,
            hex_colour="#C414C7",
            type="dummy type",
            description="dummy description",
        )
        db.session.add(ct_1)
        db.session.commit()

        ct_id2 = uuid.uuid4()
        ct_2 = ContactType(
            id=ct_id2,
            hex_colour="#FFFFFF",
            type="new dummy type",
            description="new dummy description",
        )
        db.session.add(ct_2)
        db.session.commit()

        ct_id3 = uuid.uuid4()
        ct_3 = ContactType(
            id=ct_id3,
            hex_colour="#FF5733",
            type="different dummy type",
            description="different dummy description",
        )
        db.session.add(ct_3)
        db.session.commit()

        response = self.client.get("/contact_type")
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        self.assertEqual(len(json_data), 3)

        self.assertEqual(json_data[0]["type"], "dummy type")
        self.assertEqual(json_data[1]["hex_colour"], "#FFFFFF")
        self.assertEqual(json_data[2]["description"], "different dummy description")

    def test_get_contacts_by_contact_type(self):
        ct_id = uuid.uuid4()

        # get contacts by contact_type that does not exist
        response = self.client.get("/contact_type/{}/contacts".format(ct_id))
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
        ct = ContactType(
            id=ct_id,
            hex_colour="#fffffff",
            type="dummy type",
            description="dummy description",
            contacts=[c0, c1],
        )
        db.session.add(ct)
        db.session.commit()

        # get contacts by contact_type that exists
        response = self.client.get("/contact_type/{}/contacts".format(ct_id))
        json_response = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 2)
        actual_ids = [json_response[0]["id"], json_response[1]["id"]]
        expected_ids = [str(c0_id), str(c1_id)]
        self.assertCountEqual(expected_ids, actual_ids)

    def test_edit_contact_type_route(self):
        ct_id = uuid.uuid4()
        ct = ContactType(
            id=ct_id,
            hex_colour="#C414C7",
            type="dummy type",
            description="dummy description",
        )
        db.session.add(ct)
        db.session.commit()

        # update a contact_type with empty arguments
        response = self.client.put(
            "/contact_type/{}".format(ct_id),
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, 400)

        # new arguments for contact_type
        edited_ct = {
            "hex_colour": "#ffffff",
            "type": "new dummy type",
            "description": "new dummy description",
        }

        # edit a contact_type does exist
        response = self.client.put(
            "/contact_type/{}".format(ct_id),
            content_type="application/json",
            data=json.dumps(edited_ct),
        )
        self.assertEqual(response.status_code, 200)

        # empty arguments for a contact tyoe that exists
        empty_ct = {
            "hex_colour": "",
            "type": "",
            "description": "",
        }

        response = self.client.put(
            "/contact_type/{}".format(ct_id),
            content_type="application/json",
            data=json.dumps(empty_ct),
        )
        self.assertEqual(response.status_code, 400)

        # editing a contact_type that doesn't exist
        response = self.client.put(
            "/contact_type/{}".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps(edited_ct),
        )
        self.assertEqual(response.status_code, 404)
