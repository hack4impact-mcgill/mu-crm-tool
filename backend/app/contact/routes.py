from flask import jsonify, abort, request
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


# edit a contact
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
    # if all values are None, nones = True, if not nones = False
    nones = not all(data.values())

    if (
        not data
        or nones
        or (
            name == ""
            and email == ""
            and secondary_email == ""
            and cellphone == ""
            and role == ""
            and organization == ""
            and neighbourhood == ""
        )
    ):
        abort(400, "No fields to update")

    if name is not None and name != "":
        contact.name = name

    if email is not None and email != "":
        contact.email = email

    if secondary_email is not None and secondary_email != "":
        contact.secondary_email = secondary_email

    if cellphone is not None and cellphone != "":
        contact.cellphone = cellphone

    if role is not None and role != "":
        contact.role = role

    if organization is not None and organization != "":
        contact.organization = organization

    if neighbourhood is not None and neighbourhood != "":
        contact.neighbourhood = neighbourhood

    db.session.add(contact)
    db.session.commit()

    return jsonify(contact.serialize)
