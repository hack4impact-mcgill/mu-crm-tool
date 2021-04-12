from flask import jsonify, abort
from app import db
from app.models import Contact, ContactType
from . import contact

# delete a contact by id
@contact.route("/<uuid:id>", methods=["DELETE"])
def delete_contact_type(id):
    contact = Contact.query.filter_by(id=id).first()
    if contact is None:
        abort(404, "No contact found with specified ID.")

    db.session.delete(contact)
    db.session.commit()

    return jsonify(contact.serialize)


# get a contact's contact types
@contact.route("/<uuid:id>/contact-types", methods=["GET"])
def get_contact_contact_types(id):
    contact = Contact.query.filter_by(id=id).first()
    if contact is None:
        abort(404, "No contact found with specified ID.")

    return jsonify(ContactType.serialize_list(contact.contact_types))
