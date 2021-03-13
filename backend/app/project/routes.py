from flask import jsonify, request, abort
from app import db
from app.models import Project, Contact
from . import project


# create a new project
@project.route("", methods=["POST"])
def create_project():
    data = request.get_json(force=True)
    address = data.get("address")
    city = data.get("city")
    province = data.get("province")
    postal_code = data.get("postal_code")
    neighbourhood = data.get("neighbourhood")
    year = data.get("year")
    name = data.get("name")
    type = data.get("type")
    is_completed = data.get("is_completed")

    # check if all fields are empty, if so it's a garbage post
    if (
        address == ""
        and city == ""
        and province == ""
        and postal_code == ""
        and neighbourhood == ""
        and year is None
        and name == ""
        and type == ""
        and (is_completed == False or is_completed == True)
    ):
        abort(400, "Cannot have all empty fields for a new project")

    new_project = Project(
        address=address,
        city=city,
        province=province,
        postal_code=postal_code,
        neighbourhood=neighbourhood,
        year=year,
        name=name,
        type=type,
        is_completed=is_completed,
    )

    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.serialize)


# helper returns all project types;
@project.route("/types", methods=["GET"])
def get_all_project_types():
    types = []
    for project in Project.query.distinct(Project.type):
        types.append(project.type)
    return jsonify(types)


# get projects according to specified arguments (if any)
@project.route("", methods=["GET"])
def get_projects():
    projects = Project.query.all()

    type = request.args.get("type")
    if type is not None:
        if type == "":
            abort(404, "Project type invalid")

        projects = list(filter(lambda project: (project.type == type), projects))

    is_completed = request.args.get("isCompleted")
    if is_completed is not None:
        if is_completed == "":
            abort(404, "completion status invalid")

        projects = list(
            filter(lambda project: (project.is_completed == is_completed)), projects
        )

    # add additional request arguments below

    return jsonify(Project.serialize_list(projects))


# get a project by id
@project.route("/<uuid:id>", methods=["GET"])
def get_project_by_id(id):
    project = Project.query.filter_by(id=id).first()
    if project is None:
        abort(404, "No project found with specified ID.")

    return jsonify(project.serialize)


# update a project by id
@project.route("/<uuid:id>", methods=["PUT"])
def update_project(id):
    data = request.get_json(force=True)
    address = data.get("address")
    city = data.get("city")
    province = data.get("province")
    postal_code = data.get("postal_code")
    neighbourhood = data.get("neighbourhood")
    year = data.get("year")
    name = data.get("name")
    type = data.get("type")
    is_completed = data.get("is_completed")

    project = Project.query.filter_by(id=id).first()
    if project is None:
        abort(404, "No project with specified ID")

    if address is not None:
        project.address = address

    if city is not None:
        project.city = city

    if province is not None:
        project.province = province

    if postal_code is not None:
        project.postal_code = postal_code

    if neighbourhood is not None:
        project.neighbourhood = neighbourhood

    if year is not None:
        project.year = year

    if name is not None:
        project.name = name

    if type is not None:
        project.type = type

    if is_completed is not None:
        project.is_completed = is_completed

    if not data:
        abort(400, "No fields to update")

    db.session.add(project)
    db.session.commit()
    return jsonify(project.serialize)


# get all contacts by project id
@project.route("/<uuid:id>/contacts", methods=["GET"])
def get_all_contacts_by_project(id):
    project = Project.query.filter_by(id=id).first()
    if project is None:
        abort(404, "No project found with specified ID.")
    contacts = project.contacts

    return jsonify(Contact.serialize_list(contacts))
