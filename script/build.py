"""
@author: simon.lambin

Build script called by rez-build
"""

import shutil
import sys
import os


def build(source_path, build_path, install_path, targets):
    src = os.path.join(source_path, "silex_client")
    config = os.path.join(source_path, "package.py")
    lint = os.path.join(source_path, ".pylintrc")
    # unit = os.path.join(source_path, "pytest.ini")

    # Copy the source to the build location
    if os.path.exists(build_path):
        # Clear the build folder
        try:
            shutil.rmtree(os.path.join(build_path, "silex_client"))
            os.remove(os.path.join(build_path, "package.py"))
            os.remove(os.path.join(build_path, ".pylintrc"))
            os.remove(os.path.join(build_path, "pytest.ini"))
        except Exception as ex:
            print("WARNING : Could not clear the build folder")
            print(ex)

    shutil.copytree(src, os.path.join(build_path, "silex_client"))
    shutil.copy(config, build_path)
    shutil.copy(lint, build_path)
    # shutil.copy(unit, build_path)

    # Copy the source to the install location
    if "install" in (targets or []):
        if os.path.exists(install_path):
            # Clear the install folder
            try:
                shutil.rmtree(install_path)
            except Exception as ex:
                print("WARNING : Could not clear the install folder")
                print(ex)

        shutil.copytree(src, os.path.join(install_path, "silex_client"))
        shutil.copy(config, install_path)
        shutil.copy(lint, install_path)
        # shutil.copy(unit, install_path)


if __name__ == "__main__":
    build(
        source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path=os.environ["REZ_BUILD_PATH"],
        install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
        targets=sys.argv[1:],
    )
