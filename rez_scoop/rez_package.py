"""
@author: simon.lambin

CLass definition that can be used to create a rez package
from a scoop package
"""
import os
import shutil

from rez.package_maker import make_package

from rez_scoop.utils.log import logger
from rez_scoop.scoop_package import ScoopPackage
from rez.config import config


class RezPackage:
    """
    Create a rez package from a scoop package
    """

    def __init__(self, scoop_package: ScoopPackage) -> None:
        self.name = scoop_package.name
        self.scoop_package = scoop_package

        # Transfer all the attributes
        self.package_attributes = {}
        for attribute in ("version", "requires", "url", "description", "variants"):
            if hasattr(scoop_package, attribute):
                scoop_attribute = getattr(scoop_package, attribute)
                self.package_attributes[attribute] = scoop_attribute
            else:
                logger.warning("Attribute %s not found on scoop package", attribute)

        # Set all the commands
        commands = set()

        # Set all the binaries
        for path, alias, args in scoop_package.binaries:
            # Add the binaries to the path environment variable
            path = path.replace(os.sep, "/")
            dirname = os.path.dirname(path).replace(os.sep, "/")
            commands.add(f"env.PATH.prepend('{dirname}')")
            # Add the aliases
            if alias is not None:
                commands.add(f"alias({alias}, {path} {args})")

        # Add the custom environment variables
        for key, value in scoop_package.environments:
            commands.add(f"env.{key}.prepend('{value}')")

        # Handle the case of no commands being present
        if not commands:
            commands.add("pass")

        self.package_attributes["commands"] = "\n".join(commands)

    def install(self, path=None) -> None:
        """
        Install the package localy by creating a packages.py file and copying the required files
        """

        if path is None:
            # First set the package to local package
            path = config.local_package_path
            # Override if there is a package path with the word scoop in it
            for package_path in config.packages_path:
                if "scoop" in str(package_path).lower():
                    path = package_path

        if not os.path.isdir(path):
            try:
                os.mkdir(path)
            except OSError:
                logger.error("Could not create the package base directory : %s", path)
                return

        # Install the package
        with make_package(self.name, path) as package:
            for attribute_name, attribute_value in self.package_attributes.items():
                setattr(package, attribute_name, attribute_value)

            logger.info("Installing %s", package)

        for installed_variant in package.installed_variants:
            # Copy the app in the rez package
            try:
                shutil.copytree(self.scoop_package.path, installed_variant.root)
            except OSError:
                logger.error(
                    "Could not copy the scoop package content in the rez package"
                )
                return

            logger.info(
                "Package %s installed at %s", installed_variant, installed_variant.root
            )
