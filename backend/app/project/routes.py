from flask import Flask, jsonify, request
from . import project

# get all items
@project.route("", methods=["GET"])
def get_items():
    projects = project.query.all()
    return jsonify(project.serialize_list(projects))
