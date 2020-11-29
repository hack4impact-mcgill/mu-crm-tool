from flask import abort, jsonify
from app.models import Project, db
from sqlalchemy import distinct
from . import project

# helper returns all project types;
@project.route("/project/types", methods=["GET"])
def get_all_project_types():
    types = []
    for type in Project.query.distinct(Project.type):
        types.append(Project.type)
    return jsonify(types)


# return projects with the specified type
@project.route("/project/<type>", method=["GET"])
def get_projects_of_type(type):
    if type is None:
        abort(404, "Project type invalid")
    else:
        # this returns None if the project type doesn't exist in the database
        exists = db.session.query(Project.type).filter_by(type=type).scalar()
        if exists is None:
            abort(404, "Project type invalid")
        else:
            projects = Project.query.filter_by(type=type)
            if projects is None:
                abort(404, "No project found with specified project type")
            else:
                return jsonify(Project.serialize_list(projects))
