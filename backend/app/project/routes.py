from flask import Flask, jsonify, request
from . import project

# get all projects
@project.route("", methods=["GET"])
def get_projects():
    projects = project.query.all()
    return jsonify(project.serialize_list(projects))
