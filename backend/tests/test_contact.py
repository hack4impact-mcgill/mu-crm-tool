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

    def test_get_contact_contact_types(self):
        c_id = uuid.uuid4()

        # get a non-existent contact's contact types
        response = self.client.get("/contact/{}/contact-types".format(c_id))
        self.assertEqual(response.status_code, 404)

        c = Contact(
            id=c_id,
            name="dummy name",
            email="dummy email",
            cellphone="dummy cellphone",
            role="dummy role",
            organization="dummy organization",
            neighbourhood="dummy neighbourhood",
        )
        ct0_id = uuid.uuid4()
        ct0 = ContactType(
            id=ct0_id,
            hex_colour="#fffffff",
            type="dummy type",
            description="dummy description",
            contacts=[c],
        )
        ct1_id = uuid.uuid4()
        ct1 = ContactType(
            id=ct1_id,
            hex_colour="#ddddddd",
            type="dummy type 1",
            description="dummy description 1",
            contacts=[c],
        )
        db.session.add_all([ct0, ct1])
        db.session.commit()

        # get a non-existent contact's contact types
        response = self.client.get("/contact/{}/contact-types".format(c_id))
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(len(json_response), 2)
        actual_ids = [json_response[0]["id"], json_response[1]["id"]]
        expected_ids = [str(ct0_id), str(ct1_id)]
        self.assertCountEqual(expected_ids, actual_ids)

    # test edit a contact
    def test_edit_a_contact(self):
        dummy_ct_id = uuid.uuid4()
        dummy_ct = ContactType(
            id=dummy_ct_id,
            hex_colour="#ffffff",
            type="dummy type",
            description="dummy description",
        )

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
        )

        dummy_ct_id = uuid.uuid4()
        dummy_ct = ContactType(
            id=dummy_ct_id,
            hex_colour="#ffffff",
            type="dummy type",
            description="dummy description",
            contacts=[c],
        )

        db.session.add(dummy_ct)
        db.session.commit()

        # Ensuring contact is added for contact_type
        contact_type = ContactType.query.filter_by(id=dummy_ct_id).first()
        self.assertEqual(len(contact_type.contacts), 1)

        update_obj = {
            "name": "edited name",
            "email": "edited email",
            "secondary_email": "edited secondary email",
            "cellphone": "edited cellphone",
            "role": "edited role",
            "organization": "edited organization",
            "neighbourhood": "edited neighbourhood",
        }

        # edit a contact with valid arguments
        response = self.client.put(
            "/contact/{}".format(c_id),
            content_type="application/json",
            data=json.dumps(update_obj),
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertDictContainsSubset(update_obj, json_response)

        empty_obj = {
            "name": "",
            "email": "",
            "secondary_email": "",
            "cellphone": "",
            "role": "",
            "organization": "",
            "neighbourhood": "",
        }

        # edit a contact with invalid arguments
        response = self.client.put(
            "/contact/{}".format(c_id),
            content_type="application/json",
            data=json.dumps(empty_obj),
        )
        self.assertEqual(response.status_code, 400)

        # edit a contact with an empty dict
        response = self.client.put(
            "/contact/{}".format(c_id),
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, 400)

        # edit a contact that does not exist
        response = self.client.put(
            "/contact/{}/edit".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, 404)

    # testing creating a contact
    def test_create_a_contact(self):
        dummy_ct_id = uuid.uuid4()
        dummy_ct = ContactType(
            id=dummy_ct_id,
            hex_colour="#ffffff",
            type="dummy type",
            description="dummy description",
            contacts=[],
        )
        db.session.add(dummy_ct)
        db.session.commit()

        # creating a contact with valid inputs
        response = self.client.post(
            "/contact",
            json={
                "name": "dummy name",
                "email": "dummy email",
                "secondary_email": "dummy secondary email",
                "cellphone": "dummy cell phone",
                "role": "dummy role",
                "organization": "dummy organization",
                "neighbourhood": "dummy neighbourhood",
                "contact_type": dummy_ct_id,
            },
        )
        self.assertEqual(response.status_code, 200)
        c = json.loads(response.get_data(as_text=True))

        # check that the contact has been properly added
        self.assertIsNotNone(Contact.query.filter_by(id=c["id"]).first())

        # creating a contact with invalid fields
        response = self.client.post(
            "/contact",
            json={
                "name": "dummy name",
                "email": "",
                "secondary_email": "dummy secondary email",
                "cellphone": "dummy cell phone",
                "role": "dummy role",
                "organization": "dummy organization",
                "neighbourhood": "dummy neighbourhood",
                "contact_type": dummy_ct_id,
            },
        )
        self.assertEqual(response.status_code, 400)

        # creating a contact with only required fields
        response = self.client.post(
            "/contact",
            json={
                "name": "dummy name",
                "email": "dummy email",
                "cellphone": "dummy cellphone",
                "organization": "dummy organization",
                "contact_type": dummy_ct_id,
            },
        )
        self.assertEqual(response.status_code, 200)
        c = json.loads(response.get_data(as_text=True))

        # check that the contact has been properly added at the correct id
        contact_type = Contact.query.filter_by(id=c["id"]).first()

        # creating a contact with empty fields
        response = self.client.post(
            "/contact",
            json={
                "name": "",
                "email": "",
                "secondary_email": "",
                "cellphone": "",
                "role": "",
                "organization": "",
                "neighbourhood": "",
                "contact_type": "",
            },
        )
        self.assertEqual(response.status_code, 400)
