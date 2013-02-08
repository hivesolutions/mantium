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
import time
import json
import automium

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

    def pre_update(self):
        base.Base.pre_update(self)

        # in case the current build file is empty unsets
        # it so that no override to empty occurs
        if self.build_file.is_empty(): del self.build_file

        # retrieves the current time value and the recursion value for
        # the project and uses it to calculate the initial "next time"
        current_time = time.time()
        recursion = self._get_recursion()
        self.recursion = recursion
        self.next_time = current_time + recursion
        
    def schedule(self):
        ## TODO: implement this method
        # based on the schedule_project method
        return
        
    def get_latest_build(self):
        ## TODO: implement this method
        return  

    def get_run(self, schedule = False):
        def _run():
            # retrieves the current time as the initial time
            # for the build automation execution
            initial_time = time.time()
            
            # retrieves the reference to the configuration value
            # containing the path the project directory
            projects_folder = quorum.config("PROJECTS_FOLDER") 

            # "calculates" the build file path using the projects
            # folder as the base path for such calculus
            project_folder = os.path.join(projects_folder, self.name)
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
            project = Project.get(name = self.name)
            build = self.get_latest_build()
            project.result = build["result"]
            project._result = build["_result"]
            project.build_time = build.get("delta", 0)
            project._build_time = build.get("_delta", "0 seconds")
            project.builds = project.get("builds", 0) + 1
            project.save()
    
            # in case schedule flag is not set, no need to
            # recalculate the new "next time" and put the
            # the new work into the scheduler, returns now
            if not schedule: return
    
            # retrieves the recursion integer value and uses
            # it to recalculate the next time value setting
            # then the value in the project value
            recursion = project._get_recursion()
            next_time = initial_time + recursion
            project.next_time = next_time
    
            # re-saves the project because the next time value
            # has changed (flushes contents) then schedules the
            # project putting the work into the scheduler
            project.save()
            project.schedule()

        # returns the "custom" run function that contains a
        # transitive closure on the project identifier
        return _run

    def _get_recursion(self):
        return self.days * 86400\
            + self.hours * 3600\
            + self.minutes * 60\
            + self.seconds
