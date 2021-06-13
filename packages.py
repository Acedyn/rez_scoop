"""
@author: simon.lambin

Package definition for rez_scoop
"""

# pylint: skip-file
name = "rez_scoop"
timestamp = 0
version = "0.0.0"

authors = ["simon.lambin"]

description = """
    Wrapper of the scoop package manager that install scoop package as rez packages
    """

requires = ["python-3", "scoop", "logzero"]

vcs = "git"

tests = {
    "lint": {
        "command": "pylint --rcfile={root}/.pylintrc --fail-under=8 {root}/silex_client",
        "requires": ["pylint", "pytest"],
        "run_on": ["default", "pre_release"],
    },
}

build_command = "python {root}/script/build.py {install}"


def commands():
    """
    Set the environment variables for silex_client
    """
    env.PATH.append("{root}/rez_scoop")
    env.PYTHONPATH.append("{root}")
    env.REZ_SCOOP_LOG_LEVEL = "DEBUG"
