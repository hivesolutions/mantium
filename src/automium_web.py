#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Automium System
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import json
import time
import flask
import atexit
import automium
import datetime

import models
import quorum

MONGO_DATABASE = "automium"
""" The default database to be used for the connection with
the mongo database """

CURRENT_DIRECTORY = os.path.dirname(__file__)
CURRENT_DIRECTORY_ABS = os.path.abspath(CURRENT_DIRECTORY)
UPLOAD_FOLDER = os.path.join(CURRENT_DIRECTORY_ABS, "uploads")
PROJECTS_FOLDER = os.path.join(CURRENT_DIRECTORY_ABS, "projects")

app = flask.Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROJECTS_FOLDER"] = PROJECTS_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 1024 ** 3
quorum.load(
    app,
    mongo_database = MONGO_DATABASE,
    name = "automium_web.debug",
    models = models
)

start_time = int(time.time())

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template(
        "index.html.tpl",
        link = "home"
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
    projects = models.Project.find()
    return flask.render_template(
        "project_list.html.tpl",
        link = "projects",
        projects = projects
    )

@app.route("/projects/new", methods = ("GET",))
def new_project():
    return flask.render_template(
        "project_new.html.tpl",
        link = "new_project",
        project = {},
        errors = {}
    )

@app.route("/projects", methods = ("POST",))
def create_project():
    # creates the new project, using the provided arguments and
    # then saves it into the data source, all the validations
    # should be ran upon the save operation
    project = models.Project.new()
    try: project.save()
    except quorum.ValidationError, error:
        return flask.render_template(
            "project_new.html.tpl",
            link = "new project",
            project = error.model,
            errors = error.errors
        )

    return flask.redirect(
        flask.url_for("show_project", name = project.name)
    )

@app.route("/projects/<name>", methods = ("GET",))
def show_project(name):
    project = models.Project.get(name = name)
    return flask.render_template(
        "project_show.html.tpl",
        link = "projects",
        sub_link = "info",
        project = project
    )

@app.route("/projects/<name>/edit", methods = ("GET",))
def edit_project(name):
    project = models.Project.get(name = name)
    return flask.render_template(
        "project_edit.html.tpl",
        link = "projects",
        sub_link = "edit",
        project = project,
        errors = {}
    )

@app.route("/projects/<name>/edit", methods = ("POST",))
def update_project(name):
    # finds the current project and applies the provided
    # arguments and then saves it into the data source,
    # all the validations should be ran upon the save operation
    project = models.Project.get(name = name)
    project.apply()
    try: project.save()
    except quorum.ValidationError, error:
        return flask.render_template(
            "project_edit.html.tpl",
            link = "projects",
            sub_link = "edit",
            project = error.model,
            errors = error.errors
        )

    # redirects the user to the show page of the project that
    # was just updated
    return flask.redirect(
        flask.url_for("show_project", name = name)
    )

@app.route("/projects/<name>/delete", methods = ("GET", "POST"))
def delete_project(name):
    project = models.Project.get(name = name)
    project.delete()
    return flask.redirect(
        flask.url_for("projects")
    )

@app.route("/projects/<name>/run")
def run_project(name):
    # retrieves the "custom" run function to be used
    # as the work "callable", note that the schedule flag
    # is not set meaning that no schedule will be done
    # after the execution
    project = models.Project.get(name = name)
    _run = project.get_run(schedule = False)

    # inserts a new work task into the execution thread
    # for the current time, this way this task is going
    # to be executed immediately
    current_time = time.time()
    execution_thread.insert_work(current_time, _run)

    return flask.redirect(
        flask.url_for("show_project", name = name)
    )

@app.route("/projects/<name>/builds")
def builds(name):
    project = models.Project.get(name = name)
    builds = models.Build.find(project = name)
    return flask.render_template(
        "build_list.html.tpl",
        link = "projects",
        sub_link = "builds",
        project = project,
        builds = builds
    )

@app.route("/projects/<name>/builds/<id>", methods = ("GET",))
def show_build(name, id):
    project = models.Project.get(name = name)
    build = models.Build.get(project = name, id = id)
    return flask.render_template(
        "build_show.html.tpl",
        link = "projects",
        sub_link = "info",
        project = project,
        build = build
    )

@app.route("/projects/<name>/builds/<id>/delete", methods = ("GET", "POST"))
def delete_build(name, id):
    build = models.Build.get(project = name, id = id)
    build.delete()
    return flask.redirect(
        flask.url_for("builds", name = name)
    )

@app.route("/projects/<name>/builds/<id>/log", methods = ("GET",))
def log_build(name, id):
    project = models.Project.get(name = name)
    build = models.Build.get(project = name, id = id)
    log = build.log.decode("utf-8")
    return flask.render_template(
        "build_log.html.tpl",
        link = "projects",
        sub_link = "log",
        project = project,
        build = build,
        log = log
    )

@app.route("/projects/<name>/builds/<id>/files/", defaults = {"path" : "" }, methods = ("GET",))
@app.route("/projects/<name>/builds/<id>/files/<path:path>", methods = ("GET",))
def files_build(name, id, path = ""):
    project = models.Project.get(name = name)
    build = models.Build.get(project = name, id = id)

    file_path = build.get_file_path(path)
    is_directory = os.path.isdir(file_path)
    if not is_directory: return flask.send_file(file_path)

    if path and not path.endswith("/"):
        return flask.redirect(
            flask.url_for(
                "files_build", name = name, id = id, path = path + "/"
            )
        )

    files = build.get_build_files(path)
    return flask.render_template(
        "build_files.html.tpl",
        link = "projects",
        sub_link = "files",
        project = project,
        build = build,
        path = path,
        files = files
    )

@app.route("/about")
def about():
    about = _get_about()
    return flask.render_template(
        "about.html.tpl",
        link = "about",
        about = about
    )

@app.errorhandler(404)
def handler_404(error):
    return str(error)

@app.errorhandler(413)
def handler_413(error):
    return str(error)

@app.errorhandler(BaseException)
def handler_exception(error):
    return str(error)

def _get_projects():
    projects = []
    ids = os.listdir(PROJECTS_FOLDER)
    for id in ids:
        path = os.path.join(PROJECTS_FOLDER, id)
        if not os.path.isdir(path): continue
        project = _get_project(id)
        projects.append(project)
    return projects

def _get_builds(id):
    builds = []
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    builds_folder = os.path.join(project_folder, "builds")
    build_ids = os.listdir(builds_folder)
    for build_id in build_ids:
        path = os.path.join(builds_folder, build_id)
        if not os.path.isdir(path): continue
        build = _get_build(id, build_id)
        builds.append(build)
    return builds

def _get_project(id):
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    project_path = os.path.join(project_folder, "description.json")
    project_file = open(project_path, "rb")
    try: project = json.load(project_file)
    finally: project_file.close()

    next_time = datetime.datetime.fromtimestamp(project["next_time"])
    project["_next_time"] = next_time.strftime("%b %d, %Y %H:%M:%S")

    return project

def _set_project(id, project):
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    project_path = os.path.join(project_folder, "description.json")
    project_file = open(project_path, "wb")
    try: json.dump(project, project_file)
    finally: project_file.close()

def _get_build(id, build_id):
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    builds_folder = os.path.join(project_folder, "builds")
    build_folder = os.path.join(builds_folder, build_id)
    build_path = os.path.join(build_folder, "description.json")
    build_file = open(build_path, "rb")
    try: build = json.load(build_file)
    finally: build_file.close()

    result = build["result"]
    delta = build["delta"]
    start_time = datetime.datetime.fromtimestamp(build["start_time"])
    end_time = datetime.datetime.fromtimestamp(build["end_time"])
    build["_result"] = result and "passed" or "failed"
    build["_delta"] = automium.delta_string(delta)
    build["_start_time"] = start_time.strftime("%b %d, %Y %H:%M:%S")
    build["_end_time"] = end_time.strftime("%b %d, %Y %H:%M:%S")

    return build

def _get_latest_build(id):
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    builds_folder = os.path.join(project_folder, "builds")
    build_ids = os.listdir(builds_folder)
    if not build_ids: return None
    build_ids.sort(reverse = True)
    build_id = build_ids[0]
    return _get_build(id, build_id)

def _get_build_log(id, build_id):
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    builds_folder = os.path.join(project_folder, "builds")
    build_folder = os.path.join(builds_folder, build_id)
    log_path = os.path.join(build_folder, "log/automium.log")
    log_file = open(log_path, "rb")
    try: log = log_file.read()
    finally: log_file.close()

    return log

def _get_build_files(id, build_id, path = ""):
    path = path.strip("/")
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    builds_folder = os.path.join(project_folder, "builds")
    build_folder = os.path.join(builds_folder, build_id)
    full_path = os.path.join(build_folder, path)
    entries = os.listdir(full_path)
    path and entries.insert(0, "..")
    return entries

def _get_file_path(id, build_id, path):
    path = path.strip("/")
    project_folder = os.path.join(PROJECTS_FOLDER, id)
    builds_folder = os.path.join(project_folder, "builds")
    build_folder = os.path.join(builds_folder, build_id)
    full_path = os.path.join(build_folder, path)
    return full_path

def _get_about():
    current_time = int(time.time())
    about = {
        "uptime" : automium.delta_string(current_time - start_time),
        "system" : automium.resolve_os()
    }
    return about

def _get_recursion(project):
    recursion = project.get("recursion", {})
    days = recursion.get("days", 0)
    hours = recursion.get("hours", 0)
    minutes = recursion.get("minutes", 0)
    seconds = recursion.get("seconds", 0)

    return days * 86400\
        + hours * 3600\
        + minutes * 60\
        + seconds

def _get_run(id, schedule = False):
    def _run():
        # retrieves the current time as the initial time
        # for the build automation execution
        initial_time = time.time()

        # "calculates" the build file path using the projects
        # folder as the base path for such calculus
        project_folder = os.path.join(PROJECTS_FOLDER, id)
        build_path = os.path.join(project_folder, "_build")
        _build_path = os.path.join(build_path, "build.json")

        # opens the build file descriptor and parses using
        # the json parser then closes the file
        build_file = open(_build_path, "rb")
        try: configuration = json.load(build_file)
        finally: build_file.close()

        # executes the automium task using the the build path
        # and the configuration map as parameters, then sets
        # the current (execution) path as the project folder
        # so that the resulting files are placed there
        automium.run(build_path, configuration, current = project_folder)

        # retrieves the current associated project and build
        # and uses them to update the project structure with
        # the new value (then flushes the project contents)
        project = _get_project(id)
        build = _get_latest_build(id)
        project["result"] = build["result"]
        project["_result"] = build["_result"]
        project["build_time"] = build.get("delta", 0)
        project["_build_time"] = build.get("_delta", "0 seconds")
        project["builds"] = project.get("builds", 0) + 1
        _set_project(id, project)

        # in case schedule flag is not set, no need to
        # recalculate the new "next time" and put the
        # the new work into the scheduler, returns now
        if not schedule: return

        # retrieves the recursion integer value and uses
        # it to recalculate the next time value setting
        # then the value in the project value
        recursion = _get_recursion(project)
        next_time = initial_time + recursion
        project["next_time"] = next_time

        # re-saves the project because the next time value
        # has changed (flushes contents) then schedules the
        # project putting the work into the scheduler
        _set_project(id, project)
        _schedule_project(project)

    # returns the "custom" run function that contains a
    # transitive closure on the project identifier
    return _run

def _schedule_project(project):
    # retrieves the various required project attributes
    # for the scheduling process they are going to be used
    # in the scheduling process
    id = project["id"]
    next_time = project.get("next_time", time.time())

    # retrieves the "custom" run function to be used as the
    # work for the scheduler
    _run = _get_run(id, schedule = True)

    # inserts a new work task into the execution thread
    # for the next (target time)
    execution_thread.insert_work(next_time, _run)

def _schedule_projects():
    # retrieves all the currently available project and
    # schedules all of the them in the scheduler task
    projects = _get_projects()
    for project in projects: _schedule_project(project)

def run():
    # sets the debug control in the application
    # then checks the current environment variable
    # for the target port for execution (external)
    # and then start running it (continuous loop)
    debug = os.environ.get("DEBUG", False) and True or False
    reloader = os.environ.get("RELOADER", False) and True or False
    port = int(os.environ.get("PORT", 5000))
    app.debug = debug
    app.run(
        use_debugger = debug,
        debug = debug,
        use_reloader = reloader,
        host = "0.0.0.0",
        port = port
    )

    # stop the execution thread so that it's possible to
    # the process to return the calling
    execution_thread.stop()

@atexit.register
def stop_thread():
    # stop the execution thread so that it's possible to
    # the process to return the calling
    execution_thread.stop()

# creates the thread that it's going to be used to
# execute the various background tasks and starts
# it, providing the mechanism for execution
execution_thread = quorum.execution.ExecutionThread()
execution_thread.start()

# schedules the various projects currently registered in
# the system internal structures
_schedule_projects()

if __name__ == "__main__":
    run()
