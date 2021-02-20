import uuid
from flask import jsonify, request, abort
from app import db
from app.models import ContactType
from . import contact_type

# getting all contact types
@contact_type.route("", methods=["GET"])
def get_all_contact_types():
    types = ContactType.query.all()
    return jsonify(ContactType.serialize_list(types))
    

# creating contact_type
@contact_type.route("", methods=["POST"])
def create_contact_type():
    data = request.get_json(force=True)
    hex_colour = data.get("hex_colour")
    type = data.get("type")
    description = data.get("description")
    
    if hex_colour == "" and type == "" and description == "":
        abort(400, "Please fill all indicate fields")

    new_contact_type = ContactType(
        hex_colour=hex_colour, 
        type=type, 
        description=description,
        contacts=[])

    db.session.add(new_contact_type)
    db.session.commit()
    return jsonify(new_contact_type.serialize)

# delete a contact_type by id
@contact_type.route("/<uuid:id>", methods=["DELETE"])
def delete_contact_type(id):
    contact_type = ContactType.query.filter_by(id=id).first()
    if contact_type is None:
        abort(404, "No contact type found with specified ID.")

    db.session.delete(contact_type)
    db.session.commit()

    return jsonify(contact_type.serialize)
