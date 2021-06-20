"""
@author: simon.lambin

CLass definition that can be used to create a rez package
from a scoop package
"""

import os

from rez_scoop.utils.log import logger
from rez_scoop.scoop_package import ScoopPackage


class RezPackage:
    """
    Create a rez package from a scoop package
    """

    def __init__(self, scoop_package: ScoopPackage) -> None:
        self.name = scoop_package.name
