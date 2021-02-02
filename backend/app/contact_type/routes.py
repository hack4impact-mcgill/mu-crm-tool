import uuid
from flask import jsonify, request, abort
from app import db
from app.models import ContactType
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

# edit a contact_type by id
@contact_type.route("/<uuid:id>/edit", methods=["PUT"])
def edit_contact_type(id):
    data = request.get_json(force=True)
    hex_colour = data.get("hex_colour")
    type = data.get("type")
    description = data.get("description")

    contact_type = ContactType.query.filter_by(id=id).first()
    if contact_type is None:
        abort(404, "No contact type found with specified ID.")

    if hex_colour is not None:
        contact_type.hex_colour = hex_colour

    if type is not None:
        contact_type.type = type

    if description is not None:
        contact_type.description = description

    if not data:
        abort(400, "No fields to update.")

    db.session.add(contact_type)
    db.session.commit()
    return jsonify(contact_type.serialize)
