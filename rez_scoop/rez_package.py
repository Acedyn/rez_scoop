"""
@author: simon.lambin

CLass definition that can be used to create a rez package
from a scoop package
"""
import os

from rez.package_maker import PackageMaker

from rez_scoop.utils.log import logger
from rez_scoop.scoop_package import ScoopPackage


class RezPackage:
    """
    Create a rez package from a scoop package
    """

    def __init__(self, scoop_package: ScoopPackage) -> None:
        self.name = scoop_package.name

        self.maker = PackageMaker(self.name)
        # Transfer all the attributes
        for attribute in ("version", "requires", "url", "description", "variants"):
            if hasattr(scoop_package, attribute):
                scoop_attribute = getattr(scoop_package, attribute)
                setattr(self.maker, attribute, scoop_attribute)
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

        self.maker.commands = "\n".join(commands)
