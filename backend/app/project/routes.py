from app.models import Project, db
from flask import jsonify, request, abort
from app import db
from app.models import Project
from . import project

# helper returns all project types;
@project.route("/types", methods=["GET"])
def get_all_project_types():
    types = []
    for project in Project.query.distinct(Project.type):
        types.append(project.type)
    return jsonify(types)


# return projects with the specified type
@project.route("", methods=["GET"])
def get_projects_of_type():
    type = request.args.get("type")
    if type == "":
        abort(404, "Project type invalid")
    else:
        projects = []
        for project in Project.query.filter(Project.type == type):
            projects.append(project)
        return jsonify(Project.serialize_list(projects))


# get a project by id
@project.route("/<uuid:id>", methods=["GET"])
def get_project_by_id(id):
    project = Project.query.filter_by(id=id).first()
    if project is None:
        abort(404, "No project found with specified ID.")

    return jsonify(project.serialize)


# update a project by id
@project.route("/<uuid:id>/update", methods=["PUT"])
def update_project(id):
    data = request.get_json(force=True)
    address = data.get("address")
    city = data.get("city")
    province = data.get("province")
    postal_code = data.get("postal_code")
    neighbourhood = data.get("neighbourhood")
    year = data.get("year")
    name = data.get("name")
    # should we change the name of the attribute to project_type instead
    type = data.get("type")
    # subject to change as relationship between photos has not been defined
    #    try:
    #        photo = request.files["photo"]
    #    except KeyError:
    #        photo = None

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

    if not data:
        abort(400, "No fields to update")

    db.session.add(project)
    db.session.commit()
    return jsonify(project.serialize)
