import uuid
from flask import jsonify, request, abort
from app.models import Project

# update a project by id
@project.route("/<uuid:id>/update", methods=["PUT"])
def update_project(id):
    data = request.form.to_dict(flat=True)
    address = data.get("address")
    city = data.get("city")
    province = data.get("province")
    postalCode = data.get("postalCode")
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
        abort(400, "No project with specified ID")

    if address is not None:
        project.address = address

    if city is not None:
        project.city = city

    if province is not None:
        project.province = province

    if postalCode is not None:
        project.postalCode = postalCode

    if neighbourhood is not None:
        project.neighbourhood = neighbourhood

    if year is not None:
        project.year = year

    if name is not None:
        project.name = name

    if type is not None:
        project.type = type

    if (
            address == ""
            and city == ""
            and province == ""
            and postalCode == ""
            and neighbourhood == ""
            and year is None
            and name == ""
            and type == ""
        ):
            abort(400, "No fields to update")

    db.session.add(project)
    db.session.commit()
    return jsonify(project.serialize)
