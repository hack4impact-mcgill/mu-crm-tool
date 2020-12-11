rom flask import Flask, abort, jsonify, request
from . import note
from . import db
from app.models import Note

# edit a note
@note.route("/<note_uuid>/update", METHODS=["POST"])
def edit_note(id):
    # description is only updatable field
    description = request.form["description"]

    note = Note.query.filter_by(note_id=id).first()
    if note is None:
        abort(404, "No note found with specified id")
    if description is not None:
        note.description = description
    if description == "":
        abort(404, "Nothing to update")
    note.updatedDateTime = datetime.datetime.utcnow()

    return jsonify(note.serialize)


@note.route("/<note_uuid>", METHODS=["DELETE"])
def delete_note(id):
    note = Note.query.filter_by(note_id=id).first()
    if note is None:
        abort(404, "No note found with specified id")
    db.session.delete(note)
    db.session.commit()

    return jsonify(note.serialize)
   
 
    
