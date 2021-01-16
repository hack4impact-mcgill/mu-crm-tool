from flask import jsonify, request, abort
import uuid
from app import db
from app.models import Contact
from . import contact


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


@contact.route("/<uuid:id>/edit", methods=["PUT"])
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

    if name is not None:
        contact.name = name

    if email is not None:
        contact.email = email

    if secondary_email is not None:
        contact.secondary_email = secondary_email

    if cellphone is not None:
        contact.cellphone = cellphone

    if role is not None:
        contact.role = role

    if organization is not None:
        contact.organization = organization

    if neighbourhood is not None:
        contact.neighbourhood = neighbourhood

    if projects is not None:
        contact.projects = projects

    if contact is not None:
        contact.contact_type = contact.contact_type

    if not data:
        abort(400, "No feilds to update")
    
    db.session.add(contact)
    db.session.commit()

    return jsonify(contact.serialize)


# Get all projects for a specified id (Issue #15)
@contact.route("/<uuid:id>/", methods=["GET"])
def get_all_projects(id):
    contact = Contact.query.filter_by(id=id).first()
    if contact is None:
        abort(404, "No contact found with specified id")

    # might just be overthinking this but this is the correct way to retrieve
    # the data correct
    data = contact.serialize
    return data["projects"]
