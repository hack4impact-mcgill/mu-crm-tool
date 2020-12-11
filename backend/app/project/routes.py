from flask import jsonify, request, abort
from . import Project
from .. import db

# create a new project
@project.route("", methods=["POST"])
def create_project():

    data = request.get_json(force=True)
    address = data.get("address")
    city = data.get("city")
    province = data.get("province")
    postalCode = data.get("postalCode")
    neighbourhood = data.get("neighbourhood")
    year = data.get("year")
    name = data.get("name")
    type = data.get("type")

    if (
        address == ""
        or city == ""
        or province == ""
        or postalCode == ""
        or neighbourhood == ""
        or year == ""
        or name == ""
        or type == ""
    ):
        abort(400, "Cannot have empty fields for item")

    new_item = Project(
        address=address,
        city=city,
        province=province,
        postalCode=postalCode,
        neighbourhood=neighbourhood,
        year=year,
        name=name,
        type=type
    )

    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.serialize)