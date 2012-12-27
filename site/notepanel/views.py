
import flask

from . import app

import services
from services.userservice import *


@app.route("/login", methods=["POST"])
def login():
    username = flask.request.form["username"]
    password = flask.request.form["password"]
    app.logger.debug("username = %s and password = %s" % (username, password))
    if  username == "" or password == "":
        return flask.jsonify(identified=False)
    else:
        # TODO: db check*
        if UserService().login(flask.request.form["username"], flask.request.form["password"]):
            flask.session["username"] = flask.request.form["username"]
            return flask.jsonify(
                identified=True,
                username=flask.session["username"],
                email=None,
                id=None,
                boards=None)
        else:
            return flask.jsonify(identified=False)

@app.route("/logout", methods=["GET"])
def logout():
    UserService().logout(flask.session["username"])
    flask.session.pop("username", None)
    return flask.render_template("panel.html")

@app.route("/identify", methods=["GET"])
def identify():
    # TODO: db select
    if "username" in flask.session:
        return flask.jsonify(
            identified=True,
            username=flask.session["username"],
            email=None,
            id=None,
            boards=None)
    else:
        return flask.jsonify(identified=False)

@app.route("/", methods=["GET"])
def index():
    return flask.render_template("panel.html")

@app.route("/test", methods=["GET"])
def test():
    import os
    if 'MongoIP' in os.environ:
        envvar = os.environ['MongoIP'] 
    else:
        envvar = 'Tata' 
    return flask.render_template('test.html', myvar=envvar)

