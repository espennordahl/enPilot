#! /usr/bin/env python3

import sys
import logging
import argparse
import os

from enPilot.project import Project

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("projectname", help="Name of the project to create")
    args = parser.parse_args()

    project = Project(args.projectname)
    project.createOnDisk()
