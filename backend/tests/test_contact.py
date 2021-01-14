import json
import unittest
import uuid
from flask import current_app
from app import create_app, db
from app.models import Contact, ContactType


class ContactTestCase(unittest.TestCase):
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

    def test_contact_routes(self):
        dummy_ct_id = uuid.uuid4()
        dummy_ct = ContactType(
            id=dummy_ct_id,
            hex_colour="#ffffff",
            type="dummy type",
            description="dummy description",
        )

        create_obj = {
            "name": "dummy name",
            "email": "dummy email",
            "secondary_email": "dummy secondary email",
            "cellphone": "dummy cell phone",
            "role": "dummy role",
            "organization": "dummy organization",
            "neighbourhood": "dummy neighbourhood",
            "contact_type": dummy_ct,
        }

        # create a contact
        response = self.client.post(
            "/contact",
            content_type="application/json",
            data=json.dumps(create_obj),
        )
        self.assertEqual(response.status_code, 200)

        c_id = uuid.uuid4()
        c = Contact(
            id=c_id,
            name="dummy name",
            email="dummy email",
            secondary_email="dummy secondary email",
            cellphone="dummy cellphone",
            role="dummy role",
            organization="dummy organization",
            neighbourhood="dummy neighbourhood",
            contact_type=dummy_ct,
        )

        db.session.add(c)
        db.session.commit()

        # edit a contact with empty arguments
        response = self.client.put(
            "/contact/{}/edit".format(c_id),
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, 200)

        update_obj = {
            "name": "new dummy name",
            "email": "new dummy email",
            "secondary_email": "new dummy secondary email",
            "cellphone": "new dummy cell phone",
            "role": "new dummy role",
            "organization": "new dummy organization",
            "neighbourhood": "new dummy neighbourhood",
        }

        # edit a contact with valid arguments
        response = self.client.put(
            "/contact/{}/edit".format(c_id),
            content_type="application/json",
            data=json.dumps(update_obj),
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(asText=True))
        self.assertDictContainsSubset(update_obj, json_response)

        # edit a contact that does not exist
        response = self.client.put(
            "/contact/{}/edit".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, 404)

        # delete a contact that does exist
        response = self.client.delete("/contact/{}".format(c_id))
        self.assertEqual(response.status_code, 200)

        # delete a contact that does not exist
        response = self.client.delete("/contact/{}".format(uuid.uuid4()))
        self.assertEqual(response.status_code, 404)
