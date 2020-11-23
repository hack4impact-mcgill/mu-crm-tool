from flask import Flask, abort
app = Flask(__name__)


@app.route('/project/<project_name>')
def get_proeject(project_name=None):
    if project_name is None:
        abort(404, "No item found with specified ID")
    else:
        return 'do something'
