from flask import jsonify, abort
from app import db
from app.models import Contact
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

@contact.route("/<uuid:id>", methods=["PUT"])
def edit_contact(id):
    contact = Contact.query.filter_by(id=id).first()
    if contact is None:
        abort(404, "No contact found with specified id")

    data = request.get_json(force=True)
    name = data.get("name")
    email = data.get("email")
    secondary_email = data.get("secondary_email")
    cellphone = data.get("cellphone")
    role = data.get("role")
    organization = data.get("organization")
    neighbourhood = data.get("neighbourhood")
    projects = data.get("projects")
    contact_type = data.get("contact_type")

    if (name is not None and name != ""):
        contact.name = name

    if (email is not None and email != ""):
        contact.email = email

    if (secondary_email is not None and secondary_email != ""):
        contact.secondary_email = secondary_email

    if (cellphone is not None and cellphone != ""):
        contact.cellphone = cellphone

    if (role is not None and role != ""):
        contact.role = role

    if (organization is not None and organization != ""):
        contact.organization = organization

    if (neighbourhood is not None and neighbourhood != ""):
        contact.neighbourhood = neighbourhood

    if (contact_type is not None and contact_type != ""):
        contact.contact_type = contact.contact_type

    if not data:
        abort(400, "No fields to update")
    
    db.session.add(contact)
    db.session.commit()

    return jsonify(contact.serialize)
