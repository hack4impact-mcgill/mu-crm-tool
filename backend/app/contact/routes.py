from flask import jsonify, abort, request
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


# edit a contact
@contact.route("/<uuid:id>", methods=["PUT"])
def edit_contact(id):
    # get the contact
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

# creating a contact
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
    ct = data.get("contact_type")

    if (
        # check if all fields are empty
        (name == "" or name is None)
        and (email == "" or email is None)
        and (secondary_email == "" or secondary_email is None)
        and (cellphone == "" or cellphone is None)
        and (role == "" or role is None)
        and (organization == "" or organization is None)
        and (neighbourhood == "" or neighbourhood is None)
        and (ct == "" or ct is None)
        or data == {}
    ):
        abort(400, "Cannot have all empty fields for new contact")
    # check if non-nullable fields have empty arguments
    elif name == "" or email == "" or cellphone == "" or organization == "" or ct == "":
        abort(400, "Cannot create contact without specified fields")

    ct = ContactType.query.filter_by(id=ct).first()

    new_contact = Contact(
        name=name,
        email=email,
        secondary_email=secondary_email,
        cellphone=cellphone,
        role=role,
        organization=organization,
        neighbourhood=neighbourhood,
    )

    # add contact to the contact types list of contacts
    ct.contacts.append(new_contact)
    db.session.add(new_contact)
    db.session.add(ct)
    db.session.commit()
    return jsonify(new_contact.serialize)
