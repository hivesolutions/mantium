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

import os

from mantium import models

from mantium.main import app
from mantium.main import flask
from mantium.main import quorum

@app.route("/projects/<name>/builds", methods = ("GET",))
def list_builds(name):
    project = models.Project.get(name = name)
    return flask.render_template(
        "build_list.html.tpl",
        link = "projects",
        sub_link = "builds",
        project = project
    )

@app.route("/projects/<name>/builds.json", methods = ("GET",), json = True)
def list_builds_json(name):
    object = quorum.get_object(alias = True, find = True)
    builds = models.Build.find(map = True, sort = [("id", -1)], project = name, **object)
    return builds

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
        flask.url_for("list_builds", name = name)
    )

@app.route("/projects/<name>/builds/<id>/log", methods = ("GET",))
def log_build(name, id):
    project = models.Project.get(name = name)
    build = models.Build.get(project = name, id = id)
    log = build.get_log()
    log = log.decode("utf-8")
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

    files = build.get_files(path)
    return flask.render_template(
        "build_files.html.tpl",
        link = "projects",
        sub_link = "files",
        project = project,
        build = build,
        path = path,
        files = files
    )
