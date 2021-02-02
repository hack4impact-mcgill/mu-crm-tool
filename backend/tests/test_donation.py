import unittest
from app import create_app, db
from app.models import Donation
import datetime
from sqlalchemy.exc import IntegrityError


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

    def test_donation_model(self):
        failing_case = Donation(
            name="dummy",
            email="dummy@gamil.com",
            date=datetime.datetime.now(),
            donation_source="dummy",
            event="dummy",
            num_tickets=2,
        )
        db.session.add(failing_case)
        # test passes when the commit() fails due to amount field missing
        self.assertRaises(IntegrityError, db.session.commit)
