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
import glob
import setuptools

def find_data_files(source_path, target_path, patterns):
    """
    Finds data files in the given source path and maps them
    into the target path.
    The list of patterns in glob format represents the filters.

    @type source_path: String
    @param source_path: The source path to find the data files.
    @type target_path: String
    @param target_path: The target path to the data files.
    @type patterns: List
    @param patterns: The list of patterns for file matching.
    @rtype: List
    @return: The list of data file references.
    """

    # in case the source path or the target path contain
    # a glob pattern
    if glob.has_magic(source_path) or glob.has_magic(target_path):
        # raises an exception
        raise ValueError("magic not allowed in source and target")

    # creates the data files map, responsible for mapping
    # the various directories with the existent data files
    data_files_map = {}

    # iterates over all the patterns to be able to filter
    # the file that match the provided patterns
    for pattern in patterns:
        # joins the source path and the pattern
        # to create the "complete" pattern
        pattern = os.path.join(source_path, pattern)

        # iterates over all the filenames in the
        # glob pattern
        for file_name in glob.glob(pattern):
            # in case there is no file to be read
            # must skip the current loop
            if not os.path.isfile(file_name): continue

            # retrieves the relative file path between
            # the source path and the file name
            relative_file_path = os.path.relpath(file_name, source_path)

            # creates the target file path using the
            # target path and the relative path and then
            # retrieves its directory name as the path
            target_file_path = os.path.join(target_path, relative_file_path)
            path = os.path.dirname(target_file_path)

            # adds the filename to the data files map
            data_files_map.setdefault(path, []).append(file_name)

    # retrieves the data files items and then sorts
    # them according to the default order
    data_files_items = data_files_map.items()
    data_files_items = sorted(data_files_items)

    # returns the data files items
    return data_files_items

# finds the various static and template data files to be
# included in the package (this is required for non python
# files by the setuptools)
base_data_files = find_data_files("src", "", ["automium_web.wsgi"])
projects_data_files = find_data_files("src/projects", "projects", ["README.md"])
static_data_files = find_data_files("src/static", "static", ["css/*", "images/*", "js/*", "libs/*/*/*"])
templates_data_files = find_data_files("src/templates", "templates", ["*", "partials/*"])
data_files = base_data_files + projects_data_files + static_data_files + templates_data_files

# retrieves the current root directory (from the
# currently executing file) and in case its not
# the top level root directory changed the current
# executing directory into it (avoids relative path
# problems in executing setuptools)
root_directory = os.path.dirname(__file__)
if not root_directory == "": os.chdir(root_directory)

setuptools.setup(
    name = "automium_web",
    version = "0.1.1",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = "Automium System Web Interface",
    license = "GNU General Public License (GPL), Version 3",
    keywords = "automium build automation",
    url = "http://automium.com",
    zip_safe = False,
    packages = [
        "models",
        "views",
        "views.web",
        "quorum"
    ],
    scripts = [
        "scripts/pypi/automium_web.bat",
        "scripts/pypi/automium_web_pypi.py"
    ],
    py_modules = [
        "automium_web"
    ],
    package_dir = {
        "" : os.path.normpath("src")
    },
    data_files = data_files,
    install_requires = [
        "automium",
        "flask"
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ]
)
