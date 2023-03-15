# #####################################################################################
# The MIT License (MIT)
# Copyright (c) 2023 Renesas Electronics Corporation and/or its affiliates
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
# #####################################################################################
"""This file contains classes to handle projects."""

import json
import os
import pathlib
import subprocess

from common import bcolors, bashexec, findFirstOfGlob

class ProjectList(list):
    """The project list class is a python list of project items with custom initialization items and some custom print options."""

    def __init__(self, jsonFile=False, projectDirectory=False, examplesDirectory=False, verbose=False):
        """Initialize the Project using either a json file or a directory to start searching for the projects."""
        if jsonFile:
            self._initFromJsonFile(jsonFile, verbose)
        elif all([projectDirectory, examplesDirectory]):
            self._initFromDirectory(projectDirectory, examplesDirectory, verbose)
        else:
            raise Exception("To initialize a ProjectList from a json, provide argument with json file. Or to initialize a ProjectList from a directory, provide arguments projectDirectory and examplesDirectory")

    def _initFromJsonFile(self, jsonFile, verbose=False):
        """Initialize from a json file."""
        jsonFile = open(jsonFile)
        projectsData = json.load(jsonFile)
        for p in projectsData:
            self.append(Project(p, verbose=verbose))

    def _initFromDirectory(self, projectDirectory, examplesDirectory, verbose=False):
        """Initialize from a project directory and examples directory for the relative paths."""
        for dirpath, _, filenames in os.walk(projectDirectory):
            for f in filenames:
                if str(f).endswith(".uvprojx"):
                    fullpath = os.path.abspath(os.path.join(dirpath, f))
                    if verbose:
                        print("found project file: " + fullpath)
                    self.append(Project(fullpath, examplesDirectory, verbose=verbose))

class Project:
    """Projects are all of the individual cmake project projects in this repository."""

    def __init__(self, source, exdir=os.getcwd(), verbose=False):
        """Initialize the Project using either a uvprojx path or a dict."""
        # multiple constructors not officially supported by python, this is a workaround
        if type(source) == str:
            self._initFromPath(source, exdir=exdir, verbose=verbose)
        elif type(source) == dict:
            self._initFromDict(source, verbose=verbose)
        else:
            raise Exception("source type not supported")

    def _initFromPath(self, path, exdir, verbose=False):
        """Initialize the Project using the uvprojx path."""
        inPath = pathlib.Path(path)
        self.absPath = inPath.parents[1]
        self.path = str(self.absPath).replace(str(exdir), "")[1:]
        self.title = inPath.parents[1].name
        self.group = str(inPath.relative_to(exdir)).split("/")[0]
        self.uvprojxFile = inPath
        self.uvisionLogFile = self.title + "_log.txt"
        self.cmakelistsFile = findFirstOfGlob(inPath, "CMakeLists.txt")
        self.readmePath = findFirstOfGlob(inPath, "Readme.md")
        self.builddir = (
            inPath.parents[1].joinpath("build").relative_to(inPath.parents[1])
        )
        self.buildStatus = []
        if verbose:
            print("initialized ", end="")
            print(self)

    def _initFromDict(self, dict, verbose=False):
        """Initialize the Project from a dict."""
        self.absPath = pathlib.Path(dict["absPath"])
        self.path = pathlib.Path(dict["path"])
        self.title = pathlib.Path(dict["title"])
        self.group = pathlib.Path(dict["group"])
        self.uvprojxFile = pathlib.Path(dict["uvprojxFile"])
        self.uvisionLogFile = dict["uvisionLogFile"]
        if dict["cmakelistsFile"] == "":
            self.cmakelistsFile = ""
        else:
            self.cmakelistsFile = pathlib.Path(dict["cmakelistsFile"])
        self.readmePath = pathlib.Path(dict["readmePath"])
        self.builddir = pathlib.Path(dict["builddir"])
        self.buildStatus = dict["buildStatus"]

    def addBuildStatus(self, buildsystem, target, passed, binPath):
        """Add a build to the project item."""
        if not self.buildStatus:
            self.buildStatus = []
        for i in range(len(self.buildStatus)):
            if (self.buildStatus[i]["buildsystem"] == buildsystem) and (
                self.buildStatus[i]["target"] == target.name
            ):
                del self.buildStatus[i]
                break

        self.buildStatus.append(
            {
                "buildsystem": buildsystem,
                "target": target.to_json(),
                "passed": passed,
                "binPath": str(binPath),
            }
        )

    def toDictComplete(self):
        """Get the project as a dictionary."""
        return {
            "absPath": str(self.absPath),
            "path": str(self.path),
            "title": str(self.title),
            "group": str(self.group),
            "uvprojxFile": str(self.uvprojxFile),
            "uvisionLogFile": str(self.uvisionLogFile),
            "cmakelistsFile": str(self.cmakelistsFile),
            "readmePath": str(self.readmePath),
            "builddir": str(self.builddir),
            "buildStatus": self.buildStatus,
        }

    def toDictAws(self, rootdir, fortarget):
        """Get the project as a dictionary in standard Renesas AWS artifact format."""
        binPath = ""
        for b in self.buildStatus:
            if (b["target"]["name"] == fortarget.name) and (b["passed"] is True):
                binPath = b["binPath"]
        if binPath != "":
            return {
                "path": str(self.path),
                "group": str(self.group),
                "title": str(self.title),
                "readmePath": str(self.readmePath).replace(str(rootdir), "")[1:],
                "binPath": binPath,
            }
        else:
            return False

    def __repr__(self):
        """Representation of the class when printing."""
        return (
            "Project:\n\tabsPath: "
            + str(self.absPath)
            + "\n\tpath: "
            + str(self.path)
            + "\n\ttitle: "
            + str(self.title)
            + "\n\tgroup: "
            + str(self.group)
            + "\n\tuvprojxFile: "
            + str(self.uvprojxFile)
            + "\n\tuvisionLogFile: "
            + str(self.uvisionLogFile)
            + "\n\tcmakelistsFile: "
            + str(self.cmakelistsFile)
            + "\n\treadmePath: "
            + str(self.readmePath)
            + "\n\tbuilddir: "
            + str(self.builddir)
            + "\n\tbuildStatus: "
            + str(self.buildStatus)
        )


