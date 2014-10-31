#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Mantium System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Mantium System.
#
# Hive Mantium System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Mantium System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Mantium System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

from mantium import models

from mantium.main import app
from mantium.main import flask
from mantium.main import quorum

@app.route("/projects", methods = ("GET",))
def list_projects():
    return flask.render_template(
        "project_list.html.tpl",
        link = "projects"
    )

@app.route("/projects.json", methods = ("GET",), json = True)
def list_projects_json():
    object = quorum.get_object(alias = True, find = True)
    projects = models.Project.find(map = True, **object)
    return projects

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
    except quorum.ValidationError as error:
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
    except quorum.ValidationError as error:
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
        flask.url_for("list_projects")
    )

@app.route("/projects/<name>/config", methods = ("GET", "POST"))
def config_project(name):
    project = models.Project.get(name = name)
    config = project.get_config()
    return flask.Response(
        config,
        mimetype = "application/json"
    )

@app.route("/projects/<name>/run")
def run_project(name):
    # retrieves the "custom" run function to be used
    # as the work "callable", note that the schedule flag
    # is not set meaning that no schedule will be done
    # after the execution
    project = models.Project.get(name = name)
    _run = project.get_run(schedule = False)

    # starts the running of the run method in a background
    # fashion (another thread) so that no blocking occurs
    quorum.run_back(_run)

    return flask.redirect(
        flask.url_for("show_project", name = name)
    )
