#! /usr/bin/env python3

import sys
import logging
import argparse
import os

from enPilot.project import Project

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project", help="Name of the project")
    parser.add_argument("shotasset", help="Name of the shot or asset")
    args = parser.parse_args()

    projects = Project.listProjects()
    if args.project not in projects:
        logging.error("Could not find {} in projects dir".format(args.project))
        raise Exception

    project = Project(args.project)

    asset = None
    if args.shotasset in project.assets:
        asset = project.assets[args.shotasset]
    elif args.shotasset in project.shots:
        asset = project.shots[args.shotasset]

    if not asset:
        logging.error("Could not find {} in shots or assets".format(args.shotasset))
        raise Exception

    os.environ["PROJECT"] = args.project
    os.environ["ASSET"] = args.shotasset

    os.chdir(asset.path)
