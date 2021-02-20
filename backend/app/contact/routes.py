from flask import jsonify, abort
from app import db
from app.models import Contact
from . import contact

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
    projects = data.get("projects")
    contact_type = data.get("contact_type")

    if (
        # all non-nullable attributes and relationships
        name == ""
        or email == ""
        or cellphone == ""
        or organization == ""
        or projects == None
        or contact_type == None
    ):
        abort(400, "Indicated fields cannot be empty")
    new_contact = Contact(
        name=name,
        email=email,
        secondary_email=secondary_email,
        cellphone=cellphone,
        role=role,
        organization=organization,
        neighbourhood=neighbourhood,
        projects=projects,
        contact_type=contact_type,
    )

    db.session.add(new_contact)
    db.session.commit()


# delete a contact by id
@contact.route("/<uuid:id>", methods=["DELETE"])
def delete_contact_type(id):
    contact = Contact.query.filter_by(id=id).first()
    if contact is None:
        abort(404, "No contact found with specified ID.")

    db.session.delete(contact)
    db.session.commit()

    return jsonify(contact.serialize)
