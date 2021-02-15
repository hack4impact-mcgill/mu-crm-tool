from flask import request, abort, jsonify
from app.models import Donation
from . import donation


@donation.route("", methods=["GET"])
def get_donation_amounts_by_email():
    donations = Donation.query.all()

    email = request.args.get("email")
    if email is not None:
        if email == "":
            abort(404, "Invalid email address")

        filtered_donation = list(
            filter(lambda donations: (donations.email == email), donations)
        )

        # if no email is found in the database
        if not filtered_donation:
            abort(404, "Invalid email address")

        total_amount = sum([donation.amount for donation in filtered_donation])
        return jsonify(total_amount=total_amount)
