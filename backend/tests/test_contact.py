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

    def test_delete_a_contact(self):
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
        db.session.add(ct)
        db.session.commit()

        # Ensuring contact is added for contact_type
        contact_type = ContactType.query.filter_by(id=ct_id).first()
        self.assertEqual(len(contact_type.contacts), 1)

        # deleting a contact that exists
        response = self.client.delete("/contact/{}".format(c_id))
        self.assertEqual(response.status_code, 200)

        # Ensuring contact is removed for contact_type
        contact_type = ContactType.query.filter_by(id=ct_id).first()
        self.assertEqual(len(contact_type.contacts), 0)

        # deleting a contact that does not exist
        response = self.client.delete("/contact/{}".format(c_id))
        self.assertEqual(response.status_code, 404)

    # testing creating a contact
    def test_create_a_contact(self):
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
