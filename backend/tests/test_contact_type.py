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
        response = self.client.put("/contact_type/{}/edit".format(id),
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
        response = self.client.put("/contact_type/{}/edit".format(ct_id),
            content_type="application/json",
            data=json.dumps(edited_ct)

        )
        self.assertEqual(response.status_code, 200)

        # editing a contact_type that doesn't exist
        response = self.client.put(
            "/contact_type/{}/edit".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps(edited_ct),
        )
        self.assertEqual(response.status_code, 404)

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

        # update a contact_type with empty arguments
        response = self.client.put("/contact_type/{}/edit".format(id),
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
        response = self.client.put("/contact_type/{}/edit".format(ct_id),
            content_type="application/json",
            data=json.dumps(edited_ct)

        )
        self.assertEqual(response.status_code, 200)

        # editing a contact_type that doesn't exist
        response = self.client.put(
            "/contact_type/{}/edit".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps(edited_ct),
        )
        self.assertEqual(response.status_code, 404)
        
        # get contacts by contact_type that exists
        response = self.client.get("/contact_type/{}/contacts".format(ct_id))
        json_response = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 2)
        actual_ids = [json_response[0]["id"], json_response[1]["id"]]
        expected_ids = [str(c0_id), str(c1_id)]
        self.assertCountEqual(expected_ids, actual_ids)
