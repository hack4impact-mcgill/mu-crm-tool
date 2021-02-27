from flask import request, abort, jsonify
from . import donation
from .. import db
from app.models import Donation
import uuid
from datetime import datetime

# Create new donation
@donation.route("", methods=["POST"])
def create_donation():
    # Load request to data
    data = request.get_json(force=True)
    # Assign id new uuid, and set date to now
    id = uuid.uuid4()
    date = datetime.now()
    # Load data to the corresponding variables
    name = data.get("name")
    email = data.get("email")
    donation_source = data.get("donation_source")
    event = data.get("event")
    num_tickets = data.get("num_tickets")
    added_by = data.get("added_by")
    amount = data.get("amount")
    # Check if nullable=False columns are empty
    if name == "" or donation_source == "" or email == "":
        abort(400, "Name, doantion_source, and email can not be empty")
    new_donation = Donation(
        id=id,
        name=name,
        email=email,
        date=date,
        donation_source=donation_source,
        event=event,
        num_tickets=num_tickets,
        added_by=added_by,
        amount=amount,
    )
    db.session.add(new_donation)
    db.session.commit()
    return jsonify(new_donation.serialize)


# Update Donation
@donation.route("/<uuid:donation_uuid>", methods=["PUT"])
def update_donation(donation_uuid):
    data = request.get_json(force=True)
    donation = Donation.query.get(donation_uuid)
    if donation is None:
        abort(404, "No donation found with specified UUID")
    name = data.get("name")
    email = data.get("email")
    date = data.get("date")
    donation_source = data.get("donation_source")
    event = data.get("event")
    num_tickets = data.get("num_tickets")
    added_by = data.get("added_by")
    amount = data.get("amount")
    if (
        (name == "" or name is None)
        and (email == "" or email is None)
        and date is None
        and (donation_source == "" or donation_source is None)
        and (event == "" or event is None)
        and num_tickets is None
        and (added_by == "" or added_by is None)
        and (amount is None)
    ):
        abort(400, "No donation fields to update")
    if name:
        donation.name = name
    if email:
        donation.email = email
    if date:
        donation.date = date
    if donation_source:
        donation.donation_source = donation_source
    if event:
        donation.event = event
    if num_tickets:
        donation.num_tickets = num_tickets
    if added_by:
        donation.added_by = added_by
    if amount:
        donation.amount = amount
    db.session.add(donation)
    db.session.commit()
    return jsonify(donation.serialize)


# Delete Donation (#why_so_heartless)
@donation.route("/<uuid:donation_uuid>", methods=["DELETE"])
def delete_donation(donation_uuid):
    donation = Donation.query.get(donation_uuid)
    if donation is None:
        abort(404, "No donation found with specified UUID")
    db.session.delete(donation)
    db.session.commit()
    return jsonify(donation.serialize)


@donation.route("/amount", methods=["GET"])
def get_donation_amount():
    donations = Donation.query.all()

    email = request.args.get("email")
    if email is not None:

        filtered_donation = list(
            filter(lambda donation: (donation.email == email), donations)
        )

        # if no email is found in the database
        if not filtered_donation:
            abort(404, "Invalid email address")

        total_amount = sum([donation.amount for donation in filtered_donation])
        return jsonify(total_amount=total_amount)
