from setuptools import setup

setup(
    name="rez_scoop",
    version="1.0.0",    
    description="",
    url="https://github.com/Acedyn/rez_scoop.git",
    author="Simon Lambin",
    author_email="slambin@artfx.fr",
    packages=["rez_scoop"],
    install_requires=["logzero", "rez"],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
