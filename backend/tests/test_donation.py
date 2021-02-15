import unittest
from app import create_app, db
from app.models import Donation
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
        failing_case = Donation(
            name="dummy",
            email="dummy@gamil.com",
            date=datetime.datetime.now(),
            donation_source="dummy",
            event="dummy",
            num_tickets=2,
        )
        passing_case = Donation(
            name="dummy",
            email="dummy@gamil.com",
            date=datetime.datetime.now(),
            donation_source="dummy",
            event="dummy",
            num_tickets=2,
            amount=200,
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
        email_address = "dummy@gamil.com"
        d1 = Donation(
            name="dummy",
            email=email_address,
            date=datetime.datetime.now(),
            donation_source="dummy",
            event="dummy",
            num_tickets=2,
            amount=200,
        )
        d2 = Donation(
            name="dummy2",
            email=email_address,
            date=datetime.datetime.now(),
            donation_source="dummy2",
            event="dummy2",
            num_tickets=2,
            amount=300,
        )

        db.session.add_all([d1, d2])
        db.session.commit()

        # testing passing case
        response = self.client.get("/donation?email={}".format(email_address))
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertEqual(json_response["total_amount"], 500)

        # testing with missing param
        response2 = self.client.get("/donation?email=")
        self.assertEqual(response2.status_code, 404)

        # testing with email that doesn't exist in the database
        bad_email = "bad_email@gmail.com"
        response3 = self.client.get("/donation?email={}".format(bad_email))
        self.assertEqual(response3.status_code, 404)
