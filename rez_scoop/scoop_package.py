"""
@author: simon.lambin

CLass definition that can be used to install scoop packages, parse
and store its metadata
"""

import subprocess
import os
import json
from typing import Dict, List

from rez.utils.platform_ import platform_

from rez_scoop.utils.log import logger


class ScoopPackage:
    """
    Install and store metadata of a scoop package
    """

    def __init__(self, package_name: str) -> None:
        self.name = package_name
        self.installed = False
        self.scoop_root = os.getenv("SCOOP") or f"{os.getenv('HOME')}{os.sep}scoop"
        self.path = os.path.join(self.scoop_root, "apps", self.name)
        self._metadata = None

    def install(self) -> None:
        """
        Install the package calling scoop throught a subprocess
        """

        if self.installed:
            logger.info("Scoop package already installed")
            return

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
        if self._metadata is not None:
            return self._metadata

        # Initialize metadata
        self._metadata = {}
        # Find wich bucket the package belong to
        buckets = os.listdir(os.path.join(self.scoop_root, "buckets"))
        metadata_json = None
        for bucket in buckets:
            metadata_file = os.path.join(str(buckets), bucket, f"{self.name}.json")
            if os.path.isfile(metadata_file):
                with open(metadata_file) as file:
                    metadata_json = json.load(file)
                    break

        if metadata_json is None:
            logger.error("Could not find package metadata")
            return self._metadata

        self._metadata = metadata_json
        return self._metadata

    @property
    def description(self) -> str:
        if hasattr(self.metadata, "description"):
            return self.metadata["description"]
        else:
            return "No description provided"

    @property
    def version(self) -> str:
        if hasattr(self.metadata, "version"):
            return self.metadata["description"]
        else:
            return "0.0.0"

    @property
    def url(self) -> str:
        if "url" in self.metadata:
            return self.metadata["url"]

        arch = {
            "AMD64": "64bit",
            "i686": "32bit",
        }[platform_.arch]
        return self.metadata["architecture"][arch]["url"]

    @property
    def requires(self) -> List[str]:
        if "depends" not in self.metadata:
            return []

        # The depends entry can be a list or a string
        if not isinstance(self.metadata["depends"], (tuple, list)):
            return [self.metadata["depends"]]
        else:
            return self.metadata["depends"]

    @property
    def variants(self) -> List[List[str]]:
        return [
            [f"platform-{platform_.name}", "arch-{platform_.arch}", "os-{platform_.os}"]
        ]

    @property
    def binaries(self) -> List[List[str]]:
        if "bin" not in self.metadata:
            return []

        # The bin entry can be a list or a string
        if isinstance(self.metadata["bin"], (tuple, list)):
            binaries_entries = self.metadata["bin"]
        else:
            binaries_entries = [self.metadata["bin"]]

        binaries = []
        for binaries_entry in binaries_entries:
            # Each bin can be just a string or a list
            # If they are a list they define a path, an alias, and arguments
            if not isinstance(binaries_entry, (tuple, list)):
                binaries_entry = [binaries_entry]

            filename = os.path.join(binaries_entry[0])
            alias = None
            args = []

            if len(binaries_entry) <= 2:
                alias = binaries_entry[1]

            if len(binaries_entry) <= 3:
                args = binaries_entry[2]

            binaries.append((os.path.join(self.path, filename), alias, args))

        return binaries

    @property
    def environments(self) -> List[List[str]]:

        environments = []

        # Parse the env_add_path field
        if "env_add_path" not in self.metadata:
            env_add = []
        elif isinstance(self.metadata["env_add_path"], (tuple, list)):
            env_add = self.metadata["env_add_path"]
        else:
            env_add = [self.metadata["env_add_path"]]

        for environment in env_add:
            environments.append(("PATH", os.path.join(self.path, environment)))

        # Parse the env_set field
        if "env_set" not in self.metadata:
            env_set = []
        elif isinstance(self.metadata["env_set"], (tuple, list)):
            env_set = self.metadata["env_set"]
        else:
            env_set = [self.metadata["env_set"]]

        for environment_name, environment_value in env_set:
            environments.append(
                (environment_name, environment_value.replace("$dir", self.path))
            )

        return environments
