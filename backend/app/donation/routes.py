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
    #Load data to the corresponding variables
    name = data.get("name")
    email = data.get("email")
    donationSource = data.get("donationSource")
    event = data.get("event")
    numTickets = data.get("numTickets")
    addedBy = data.get("addedBy")
    # Check if nullable=False columns are empty
    if (
        name == ""
        or donationSource == ""
        or email == ""
    ):
        abort(400, "Name, doantionSource, and email can not be empty")
    new_donation = Donation(
        id=id,
        name=name,
        email=email,
        date=date,
        donationSource=donationSource,
        event=event,
        numTickets=numTickets,
        addedBy=addedBy
    )
    db.session.add(new_donation)
    db.session.commit()
    return jsonify(new_donation.serialize)