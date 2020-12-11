from flask import Flask, jsonify, abort
from . import project
from . import db
from app.models import Project
import uuid

# delete a project
@project.route("/<project_uuid>", METHODS=["DELETE"])
# Login Required
def delete_project(id):
  project = Project.query.filter_by(project_id=id).first()
  if project is None:
    abort(404, "No project found with specified ID")
    
  db.session.delete(project)
  db.session.commit()
  
  return jsonify(project.serialize)
