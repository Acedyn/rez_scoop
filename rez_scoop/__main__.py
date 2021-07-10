import argparse
import sys

from rez_scoop.scoop_package import ScoopPackage
from rez_scoop.rez_package import RezPackage
from rez_scoop.utils.log import logger


def get_arguments() -> argparse.Namespace:
    """
    Parse the input arguments
    """

    parser = argparse.ArgumentParser(
        description="Create, remove and update scoop packages as rez packages"
    )
    parser.add_argument(
        "action",
        choices=["install", "update", "uninstall"],
        nargs=1,
        help="The action you want to perform on the package",
    )
    parser.add_argument(
        "package",
        nargs=1,
        help="The name of the package",
    )

    return parser.parse_args()


def install(package_name: str) -> None:
    """
    Install the package as a scoop package and a rez package
    """

    scoop_package = ScoopPackage(package_name)
    scoop_package.install()
    if not scoop_package.installed:
        logger.error("Scoop package could not be installed, skipping rez package")
        return
    rez_package = RezPackage(scoop_package)
    rez_package.install()


def uninstall(package_name: str) -> None:
    """
    Uninstall the package from scoop and rez
    """

    logger.warning("Uninstallation of package is not implemented yet")


def update(package_name: str) -> None:
    """
    Update the package for scoop and rez
    """

    logger.warning("Update of package is not implemented yet")


if __name__ == "__main__":
    # Get the passed arguments
    arguments = get_arguments()
    # Call the appropiate function from the arguments
    getattr(sys.modules[__name__], arguments.action[0])(arguments.package[0])
