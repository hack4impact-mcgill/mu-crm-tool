from flask import abort, jsonify
from app.models import Project, db
from sqlalchemy import distinct
from . import project

# helper returns all project types;
@project.route("/types", methods=["GET"])
def get_all_project_types():
    types = []
    for type in Project.query.distinct(Project.type):
        types.append(Project.type)
    return jsonify(types)

# this is a brief project test
@project.route("/hello", methods=["GET"])
def test():
    return "project test"


# return projects with the specified type
@project.route("/<type>", methods=["GET"])
def get_projects_of_type(type):
    if type is None:
        abort(404, "Project type invalid")
    else:
        projects = Project.query.filter_by(type=type)
        if projects is None:
            abort(404, "No project found with specified project type")
        else:
            return jsonify(Project.serialize_list(projects))
