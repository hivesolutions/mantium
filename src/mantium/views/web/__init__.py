#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Mantium System
# Copyright (C) 2008-2015 Hive Solutions Lda.
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

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

from . import base
from . import build
from . import project

from .base import index, login, do_login, about, handler_404, handler_413, handler_exception
from .build import list_builds, list_builds_json, show_build, delete_build, log_build,\
    files_build
from .project import list_projects, list_projects_json, new_project, create_project,\
    show_project, edit_project, update_project, delete_project, config_project, run_project
