from flask import jsonify, abort, request
from app import db
from app.models import Contact, ContactType
from . import contact
import uuid


# create a contact
@contact.route("", methods=["POST"])
def create_contact():
    data = request.get_json(force=True)
    name = data.get("name")
    email = data.get("email")
    secondary_email = data.get("secondary_email")
    cellphone = data.get("cellphone")
    role = data.get("role")
    organization = data.get("organization")
    neighbourhood = data.get("neighbourhood")
    ct = data.get("contact_type")

    if (
        # check if all fields are empty
        (name == "" or name is None)
        and (email == "" or email is None)
        and (secondary_email == "" or secondary_email is None)
        and (cellphone == "" or cellphone is None)
        and (role == "" or role is None)
        and (organization == "" or organization is None)
        and (neighbourhood == "" or neighbourhood is None)
        and (ct == "" or ct is None)
        or data == {}
    ):
        abort(400, "Cannot have all empty fields for new contact")
    # check if non-nullable fields have empty arguments
    elif name == "" or email == "" or cellphone == "" or organization == "" or ct == "":
        abort(400, "Cannot create contact without specified fields")

    ct = ContactType.query.filter_by(id=ct).first()

    new_contact = Contact(
        name=name,
        email=email,
        secondary_email=secondary_email,
        cellphone=cellphone,
        role=role,
        organization=organization,
        neighbourhood=neighbourhood,
    )

    # add contact to the contact types list of contacts
    ct.contacts.append(new_contact)
    db.session.add(new_contact)
    db.session.commit()
    return jsonify(new_contact.serialize)


# delete a contact by id
@contact.route("/<uuid:id>", methods=["DELETE"])
def delete_contact_type(id):
    contact = Contact.query.filter_by(id=id).first()
    if contact is None:
        abort(404, "No contact found with specified ID.")

    db.session.delete(contact)
    db.session.commit()

    return jsonify(contact.serialize)
