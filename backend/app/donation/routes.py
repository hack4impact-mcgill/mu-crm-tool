from flask import request, abort, jsonify
from . import donation
from .. import db
from app.models import Donation
import uuid
from datetime import datetime

# Get all donations of user_id
@donation.route("/donations/<user_uuid>", methods=["GET"])
def get_denoations_for_user(user_uuid):
    # Look for all donations of "user_id"
    donations = Donation.query.filter_by(added_by=user_uuid).all()
    return jsonify(Donation.serialize_list(donations))


# Create new donation
@donation.route("/create-donation", methods=["POST"])
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
    )
    db.session.add(new_donation)
    db.session.commit()
    return jsonify(new_donation.serialize)


# Update Donation
@donation.route("/update_dontation/<donation_uuid>", methods=["PUT"])
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
    if (
        name == ""
        and email == ""
        and date is None
        and donation_source == ""
        and event == ""
        and num_tickets is None
        and added_by == ""
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
        donation.num_tickets = int(num_tickets)
    if added_by:
        donation.added_by = added_by
    db.session.add(donation)
    db.session.commit()
    return jsonify(donation.serialize)


# Delete Donation (#why_so_heartless)
@donation.route("/<donation_uuid>", methods=["DELETE"])
def delete_donation(donation_uuid):
    donation = Donation.query.get(donation_uuid)
    if donation:
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