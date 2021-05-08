import unittest
import uuid
import json
from app import create_app, db
from app.models import Donation, MuUser
import datetime
from sqlalchemy.exc import IntegrityError


class DonationTestCase(unittest.TestCase):
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

    def test_donation_model(self):
        u_id = uuid.uuid4()
        u = MuUser(
            id=u_id,
            name="dummy",
            email="email_address",
            role="dummy role",
        )
        db.session.add(u)
        db.session.commit()
        failing_case = Donation(
            name="dummy",
            email="dummy@gamil.com",
            date=datetime.datetime.now(),
            donation_source="dummy",
            event="dummy",
            num_tickets=2,
            added_by=u_id,
        )
        passing_case = Donation(
            name="dummy",
            email="dummy@gamil.com",
            date=datetime.datetime.now(),
            donation_source="dummy",
            event="dummy",
            num_tickets=2,
            amount=200,
            added_by=u_id,
        )
        db.session.add(passing_case)
        db.session.commit()
        d = Donation.query.filter_by(name="dummy").first()
        # test serialize
        self.assertEqual(d.amount, 200)

        db.session.add(failing_case)
        # test passes when the commit() fails due to amount field missing
        self.assertRaises(IntegrityError, db.session.commit)

    def test_get_amount(self):
        u_id = uuid.uuid4()
        u = MuUser(
            id=u_id,
            name="dummy",
            email="email_address",
            role="dummy role",
        )
        db.session.add(u)
        db.session.commit()

        email_address = "dummy@gamil.com"
        d1 = Donation(
            name="dummy",
            email=email_address,
            date=datetime.datetime.now(),
            donation_source="dummy",
            event="dummy",
            num_tickets=2,
            amount=200,
            added_by=u_id,
        )
        d2 = Donation(
            name="dummy2",
            email=email_address,
            date=datetime.datetime.now(),
            donation_source="dummy2",
            event="dummy2",
            num_tickets=2,
            amount=300,
            added_by=u_id,
        )

        db.session.add_all([d1, d2])
        db.session.commit()

        # testing passing case
        response = self.client.get("/donation/amount?email={}".format(email_address))
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response["total_amount"], 500)

        # testing with missing param
        response2 = self.client.get("/donation/amount?email=")
        self.assertEqual(response2.status_code, 404)

        # testing with email that doesn't exist in the database
        bad_email = "bad_email@gmail.com"
        response3 = self.client.get("/donation/amount?email={}".format(bad_email))
        self.assertEqual(response3.status_code, 404)

    def test_create_donation(self):
        u_id = uuid.uuid4()
        u = MuUser(
            id=u_id,
            name="dummy",
            email="email_address",
            role="dummy role",
        )
        db.session.add(u)
        db.session.commit()

        response = self.client.post(
            "/donation",
            json={
                "name": "dummy name",
                "email": "dummy@email.com",
                "donation_source": "dummy source",
                "event": "dummy event",
                "num_tickets": 2,
                "added_by": u_id,
                "amount": 100,
            },
        )
        response2 = self.client.post(
            "/donation",
            json={
                "name": "dummy2 name",
                "email": "dummy2@email.com",
                "donation_source": "dummy2 source",
                "event": "dummy event 2",
                "num_tickets": 15,
                "added_by": u_id,
                "amount": 50,
            },
        )
        empty_response = self.client.post(
            "/donation",
            json={
                "name": "",
                "email": "",
                "donation_source": "",
                "event": "",
                "num_tickets": None,
                "added_by": None,
                "amount": None,
            },
        )
        # test posted correctly
        self.assertEqual(empty_response.status_code, 400)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_update_donation(self):
        u_id = uuid.uuid4()
        u = MuUser(
            id=u_id,
            name="dummy",
            email="email_address",
            role="dummy role",
        )
        db.session.add(u)
        db.session.commit()

        d_id = uuid.uuid4()
        d = Donation(
            id=d_id,
            name="dummy",
            email="dummy",
            date=datetime.datetime.now(),
            donation_source="dummy",
            event="dummy",
            num_tickets=2,
            amount=200,
            added_by=u_id,
        )
        db.session.add(d)
        db.session.commit()

        # update a donation with empty argumets
        response = self.client.put(
            "/donation/{}".format(d_id),
            content_type="application/json",
            data=json.dumps({}),
        )
        self.assertEqual(response.status_code, 400)

        # update a donation with valid arguments
        update_obj = {
            "name": "dummy2 name",
            "email": "dummy2@email.com",
            "donation_source": "dummy2 source",
            "event": "dummy event 2",
            "num_tickets": 15,
            "amount": 50,
        }
        response = self.client.put(
            "/donation/{}".format(d_id),
            content_type="application/json",
            data=json.dumps(update_obj),
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertDictContainsSubset(update_obj, json_response)

        # update a donation that does not exist
        response = self.client.put(
            "/donation/{}".format(uuid.uuid4()),
            content_type="application/json",
            data=json.dumps(update_obj),
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_donation(self):
        d_id = uuid.uuid4()

        response = self.client.delete("/donation/{}".format(d_id))
        self.assertEqual(response.status_code, 404)

        u_id = uuid.uuid4()
        u = MuUser(
            id=u_id,
            name="dummy",
            email="email_address",
            role="dummy role",
        )
        db.session.add(u)
        db.session.commit()

        d = Donation(
            id=d_id,
            name="dummy",
            email="dummy",
            date=datetime.datetime.now(),
            donation_source="dummy",
            event="dummy",
            num_tickets=2,
            amount=200,
            added_by=u_id,
        )
        db.session.add(d)
        db.session.commit()

        response2 = self.client.delete("/donation/{}".format(d_id))
        self.assertEqual(response2.status_code, 200)

    def test_csv(self):
        added_by = uuid.uuid4()
        u = MuUser(
            id=added_by,
            name="dummy",
            email="email_address",
            role="dummy role",
        )
        db.session.add(u)
        db.session.commit()
        fpaths = ["tests/assets/dummy.csv"]
        files = []
        try:
            files = [open(fpath, "rb") for fpath in fpaths]
            response = self.client.post(
                "/donation/csv",
                content_type="multipart/form-data",
                data={"added_by": added_by, "files": files},
            )
        finally:
            for f in files:
                f.close()

        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(len(json_response), 1)
