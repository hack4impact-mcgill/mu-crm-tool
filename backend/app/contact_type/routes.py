import uuid
from flask import jsonify, request, abort
from app import db
from app.models import ContactType, Contact
from . import contact_type

# delete a contact_type by id
@contact_type.route("/<uuid:id>", methods=["DELETE"])
def delete_contact_type(id):
    contact_type = ContactType.query.filter_by(id=id).first()
    if contact_type is None:
        abort(404, "No contact type found with specified ID.")

    db.session.delete(contact_type)
    db.session.commit()

    return jsonify(contact_type.serialize)


# get all contacts by contact_type
@contact_type.route("/<uuid:id>/contacts", methods=["GET"])
def get_all_contacts_by_contact_type(id):
    contact_type = ContactType.query.filter_by(id=id).first()
    if contact_type is None:
        abort(404, "No contact type found with specified ID.")
    contacts = contact_type.contacts

    return jsonify(Contact.serialize_list(contacts))
