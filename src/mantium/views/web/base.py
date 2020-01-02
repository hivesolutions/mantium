#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Mantium System
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Mantium System.
#
# Hive Mantium System is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Mantium System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Mantium System. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import time
import automium

from mantium.main import app
from mantium.main import flask

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

@app.errorhandler(Exception)
def handler_exception(error):
    return str(error)

def _get_about():
    current_time = int(time.time())
    return dict(
        uptime = automium.delta_string(current_time - start_time),
        system = automium.resolve_os()
    )
