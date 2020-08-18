#! /usr/bin/env python3

import sys
import logging
import argparse
import os

from enPilot.project import Project

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("shotname", help="Name of the shot to create")
    args = parser.parse_args()

    projectname = os.getenv("PROJECT")
    if not projectname:
        logging.error("PROJECT environment variable not set")
        raise Exception
