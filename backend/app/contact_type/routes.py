import uuid
from flask import jsonify, request, abort
from app import db
from app.models import ContactType
from . import contact_type

# creating contact_type 
@contact_type.route("", methods=["POST"])
def create_contact_type():
    data = request.get_json(force=True)
    id = int(data.get("id"))
    hex_colour = data.get("email")
    type = data.get("type")
    description = data.get("description")

    if(
        id is None 
        or hex_colour == "" 
        or type == "" 
        or description == ""
    ):
        abort(400, "Please fill all indicate fields")

    new_contact = ContactType(
    id = id, 
    hex_colour = hex_colour, 
    type = type, 
    description = description
    )

    db.session.add(new_contact)
    db.session.commit()

# edit a contact_type by id
@contact_type.route("/<uuid:id>", methods=["PUT"])
def edit_contact_type(id):
    data = request.get_json(force=True)
    id = int(data.get("id"))
    hex_colour = data.get("email")
    type = data.get("type")
    description = data.get("description")
    
    contact_type = ContactType.query.filter_by(id=id).first()
    if contact_type is None:
        abort(404, "No contact type found with specified ID.")

    if id is not None:
        contact_type.id = id

    if hex_colour is not None:
        contact_type.hex_colour = hex_colour
    
    if type is not None:
        contact_type.type = type
    
    if description is not None:
        contact_type.description = description

    if not data:
        abort(400, "No fields to update.")
        
    db.add(contact_type)
    db.session.commit()

    return jsonify(contact_type.serialize)
    
# delete a contact_type by id
@contact_type.route("/<uuid:id>", methods=["DELETE"])
def delete_contact_type(id):
    contact_type = ContactType.query.filter_by(id=id).first()
    if contact_type is None:
        abort(404, "No contact type found with specified ID.")

    db.session.delete(contact_type)
    db.session.commit()

    return jsonify(contact_type.serialize)
