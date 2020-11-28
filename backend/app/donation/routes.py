from flask import Flask, jsonify, request, abort, make_response
from . import donation
from .. import db
from app.models import Donation
import uuid
from datetime import datetime

# Get all donations of user_id
@donation.route("/donations/<user_uuid>", methods=["GET"])
def get_denoations_for_user(user_uuid):
    # Look for all donations of "user_id"
    donations = Donation.query.filter_by(addedBy=user_uuid).all()
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
    donationSource = data.get("donationSource")
    event = data.get("event")
    numTickets = data.get("numTickets")
    addedBy = data.get("addedBy")
    # Check if nullable=False columns are empty
    if name == "" or donationSource == "" or email == "":
        abort(400, "Name, doantionSource, and email can not be empty")
    new_donation = Donation(
        id=id,
        name=name,
        email=email,
        date=date,
        donationSource=donationSource,
        event=event,
        numTickets=numTickets,
        addedBy=addedBy,
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
    donationSource = data.get("donationSource")
    event = data.get("event")
    numTickets = data.get("numTickets")
    addedBy = data.get("addedBy")
    if (
        name == ""
        and email == ""
        and date is None
        and donationSource == ""
        and event == ""
        and numTickets is None
        and addedBy == ""
    ):
        abort(400, "No donation fields to update")
    if name:
        donation.name = name
    if email:
        donation.email = email
    if date:
        donation.date = date
    if donationSource:
        donation.donationSource = donationSource
    if event:
        donation.event = event
    if numTickets:
        donation.numTickets = int(numTickets)
    if addedBy:
        donation.addedBy = addedBy
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
