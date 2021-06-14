"""
@author: simon.lambin

CLass definition that can be used to install scoop packages and parse
and store its metadata
"""

import subprocess
import os
import json
from typing import Dict

from rez_scoop.utils.log import logger


class ScoopPackage:
    """
    Install and store metadata of a scoop package
    """

    def __init__(self, package_name: str) -> None:
        self.name = package_name
        self.installed = False
        self.scoop_root = os.getenv("SCOOP", f"{os.getenv('HOME')}/scoop")
        self._metadata = {}

    def install(self) -> None:
        """
        Install the package calling scoop throught a subprocess
        """
        # Check if the package is already installed
        p_search = subprocess.Popen(
            f"powershell -command scoop list {self.name}",
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        # Parse the output of the scoop list command
        for line in iter(p_search.stdout.readline, ""):
            if f" {self.name} " in str(line):
                logger.info("Scoop package already installed")
                self.installed = True
                p_search.wait()
                return

        # Wait for the search to be completed
        p_search.wait()

        # Install the package
        p_install = subprocess.Popen(
            f"powershell -command scoop install {self.name}",
            shell=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        # Parse the output of the scoop install command
        for line in iter(p_install.stdout.readline, ""):
            if f"Couldn't find manifest for '{self.name}'":
                logger.error("Scoop package does not exist")
                p_install.wait()
                return

        # Wait for the install to be completed
        p_install.wait()
        self.installed = True

    @property
    def metadata(self) -> Dict:
        """
        Get the scoop pachage's json and parse its data
        """
        # Lazy load the metadata
        if self._metadata != {}:
            return self._metadata

        # Find wich bucket the package belong to
        buckets = os.listdir(os.path.join(self.scoop_root, "buckets"))
        found_metadata = False
        for bucket in buckets:
            metadata_file = os.path.join(str(buckets), bucket, f"{self.name}.json")
            if os.path.isfile(metadata_file):
                with open(metadata_file) as file:
                    self._metadata_json = json.load(file)
                found_metadata = True
                break

        if not found_metadata:
            logger.error("Could not find package metadata")
            self._metadata = {}
            return self._metadata

        print(self._metadata)

        return self._metadata
