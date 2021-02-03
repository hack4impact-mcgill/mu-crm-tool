from flask import jsonify, abort
from app import db
from app.models import Contact
from . import contact

# create a contact
@contact.route("", methods=["POST"])
def create_contact():
    data = request.get_json(force=True)
    Name = data.get("name")
    Email = data.get("email")
    Secondary_email = data.get("secondary_email")
    Cellphone = data.get("cellphone")
    Role = data.get("role")
    Organization = data.get("organization")
    Neighbourhood = data.get("neighbourhood")
    Projects = data.get("projects")
    Contact_type = data.get("contact_type")

    if (
        # all non-nullable attributes and relationships
        Name == ""
        or Email == ""
        or Cellphone == ""
        or Organization == ""
        or Projects == None
        or Contact_type == None
    ):
        abort(400, "Indicated fields cannot be empty")
    new_contact = Contact(
        name=Name,
        email=Email,
        secondary_email=Secondary_email,
        cellphone=Cellphone,
        role=Role,
        organization=Organization,
        neighbourhood=Neighbourhood,
        projects=Projects,
        contact_type=Contact_type,
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
