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
            description="dummy description"
        )
        db.session.add(ct)
        db.session.commit()

        # deleting a contact_type that exists
        response = self.client.delete(
                "/contact_type/{}".format(ct_id))
        self.assertEqual(response.status_code, 200)

        # deleting a contact_type that does not exist
        response = self.client.delete(
                "/contact_type/{}".format(ct_id))
        self.assertEqual(response.status_code, 404)


