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

import time

import quorum

import base

class Project(base.Base):

    name = dict(
        index = True
    )

    description = dict()

    days = dict(
        type = int
    )

    hours = dict(
        type = int
    )

    minutes = dict(
        type = int
    )

    seconds = dict(
        type = int
    )

    build_file = dict(
        type = quorum.File
    )
    
    recursion = dict(
        type = int,
        private = True
    )    

    next_time = dict(
        type = int,
        private = True
    )

    def __init__(self):
        base.Base.__init__(self)
        self.days = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

    @classmethod
    def validate_new(cls):
        return super(Project, cls).validate_new() + [
            quorum.not_null("name"),
            quorum.not_empty("name"),
            quorum.not_duplicate("name", cls._name()),

            quorum.not_null("description"),
            quorum.not_empty("description"),

            quorum.not_null("build_file")
        ]

    def pre_create(self):
        base.Base.pre_create(self)

        # retrieves the current time value and the recursion value for
        # the project and uses it to calculate the initial "next time"
        current_time = time.time()
        recursion = self._get_recursion()
        self.recursion = recursion
        self.next_time = current_time + recursion

    def _get_recursion(self):
        return self.days * 86400\
            + self.hours * 3600\
            + self.minutes * 60\
            + self.seconds
