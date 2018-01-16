#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Mantium System
# Copyright (c) 2008-2018 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2018 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os

import flask #@UnusedImport

import quorum

import mantium.models

MONGO_DATABASE = "automium"
""" The default database to be used for the connection with
the mongo database """

CURRENT_DIRECTORY = os.path.dirname(__file__)
CURRENT_DIRECTORY_ABS = os.path.abspath(CURRENT_DIRECTORY)
UPLOAD_FOLDER = os.path.join(CURRENT_DIRECTORY_ABS, "uploads")
PROJECTS_FOLDER = os.path.join(CURRENT_DIRECTORY_ABS, "projects")

app = quorum.load(
    name = __name__,
    mongo_database = MONGO_DATABASE,
    logger = "mantium.debug",
    models = mantium.models,
    UPLOAD_FOLDER = UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH = 1024 ** 3
)
quorum.confs("PROJECTS_FOLDER", PROJECTS_FOLDER)

import mantium.views #@UnusedImport

# schedules the various projects currently registered in
# the system internal structures
mantium.models.Project.schedule_all()

if __name__ == "__main__":
    quorum.run(server = "netius")
else:
    __path__ = []
