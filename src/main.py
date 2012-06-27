#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Automium System
# Copyright (C) 2008 Hive Solutions Lda.
#
# This file is part of Hive Automium System.
#
# Hive Automium System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Automium System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Automium System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision: 9712 $"
""" The revision number of the module """

__date__ = "$LastChangedDate: 2010-08-10 13:42:37 +0100 (ter, 10 Ago 2010) $"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import uuid
import json
import flask
import shutil

import execution

CURRENT_DIRECTORY = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(CURRENT_DIRECTORY, "uploads")
PROJECTS_FOLDER = os.path.join(CURRENT_DIRECTORY, "projects")
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])

app = flask.Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 1024 ** 3

execution_thread = execution.ExecutionThread()
execution_thread.start()

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template(
        "index.html.tpl"
    )

@app.route("/login", methods = ("GET",))
def login():
    return flask.render_template(
        "login.html.tpl"
    )

@app.route("/login", methods = ("POST",))
def do_login():
    return flask.request.form["username"]

@app.route("/projects", methods = ("GET",))
def projects():
    # retrieves the various entries from the projects
    # folder as the various projects (identifiers)
    projects = os.listdir(PROJECTS_FOLDER)
    return flask.render_template(
        "project_list.html.tpl",
        projects = projects
    )

@app.route("/projects/new", methods = ("GET",))
def new_project():
    return flask.render_template(
        "project_new.html.tpl"
    )

@app.route("/projects", methods = ("POST",))
def create_project():
    # retrieves all the parameters from the request to be
    # handled then validated the required ones
    name = flask.request.form.get("name", None)
    description = flask.request.form.get("description", None)
    build_file = flask.request.files.get("build_file", None)

    # TODO: TENHO DE POR AKI O VALIDADOR !!!!

    # generates the unique identifier to be used to identify
    # the project reference and then uses it to create the
    # map describing the current project
    id = str(uuid.uuid4())
    project = {
        "id" : id,
        "name" : name,
        "description" : description
    }

    # creates the path to the project folder and creates it
    # in case its required then creates the path to the description
    # file of the project and dumps the json describing the project
    # into such file for latter reference
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    if not os.path.isdir(project_folder): os.makedirs(project_folder)
    project_path = os.path.join(project_folder, "description.json")
    project_file = open(project_path, "wb")
    try: json.dump(project, project_file)
    finally: project_file.close()

    # saves the build file in the appropriate location
    # folder for latter usage
    file_path = os.path.join(project_folder, "build.json")
    build_file.save(file_path)

    return flask.redirect(
        flask.url_for("show_project", id = id)
    )

@app.route("/projects/<id>", methods = ("GET",))
def show_project(id):
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    project_path = os.path.join(project_folder, "description.json")
    project_file = open(project_path, "rb")
    try: project = json.load(project_file)
    finally: project_file.close()
    return flask.render_template(
        "project_show.html.tpl",
        project = project
    )

@app.route("/projects/<id>/edit", methods = ("GET",))
def edit_project(id):
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    project_path = os.path.join(project_folder, "description.json")
    project_file = open(project_path, "rb")
    try: project = json.load(project_file)
    finally: project_file.close()
    return flask.render_template(
        "project_edit.html.tpl",
        project = project
    )

@app.route("/projects/<id>/edit", methods = ("POST",))
def update_project(id):
    # retrieves all the parameters from the request to be
    # handled then validated the required ones
    name = flask.request.form.get("name", None)
    description = flask.request.form.get("description", None)
    build_file = flask.request.files.get("build_file", None)

    # TODO: TENHO DE POR AKI O VALIDADOR !!!!

    project = {
        "id" : id,
        "name" : name,
        "description" : description
    }

    # creates the path to the project folder and creates it
    # in case its required then creates the path to the description
    # file of the project and dumps the json describing the project
    # into such file for latter reference
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    if not os.path.isdir(project_folder): os.makedirs(project_folder)
    project_path = os.path.join(project_folder, "description.json")
    project_file = open(project_path, "wb")
    try: json.dump(project, project_file)
    finally: project_file.close()

    # saves the build file in the appropriate location
    # folder for latter usage
    if build_file:
        file_path = os.path.join(project_folder, "build.json")
        build_file.save(file_path)

    return flask.redirect(
        flask.url_for("show_project", id = id)
    )

@app.route("/projects/<id>/delete", methods = ("GET", "POST"))
def delete_project(id):
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    if os.path.isdir(project_folder): shutil.rmtree(project_folder)
    return flask.redirect(
        flask.url_for("projects")
    )

@app.route("/projects/<id>/run")
def run_project(id):
    def tobias():
        print "OLA MUNDO"

    import time
    execution_thread.insert_work(time.time() + 5.0, tobias)

    return flask.redirect(
        flask.url_for("show_project", id = id)
    )

@app.route("/status")
def status():
    return "this is a status page"

@app.errorhandler(404)
def handler_404(error):
    return str(error)

@app.errorhandler(413)
def handler_413(error):
    return str(error)

if __name__ == "__main__":
    app.debug = True
    app.run(use_debugger = True, debug = True, use_reloader = False, host = "0.0.0.0")
    #app.run()
