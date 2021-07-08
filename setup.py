from setuptools import setup

# Load the README file.
with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()

setup(
    name="flowdiagram",
    #   - MAJOR VERSION 1
    #   - MINOR VERSION 0
    #   - MAINTENANCE VERSION 0
    version="1.0.0",
    author="Vaseem Khan",
    author_email='vaseemkhn18@gmail.com',
    description="Python Library to generate Sequence Diagram in Command Line or Image",
    long_description=long_description,
    packages=["flowdiagram"],
    install_requires=[
        "multipledispatch==0.6.0",
        "six",
        "Pillow"
        ],
    keywords='sequence diagram, UML diagram, flow diagram, comamnd line flow diagram',
    url='https://github.com/vaseemkhn18/FlowDiagram/',
    classifiers=[
            # Target Audience
            'Intended Audience :: Developers',
            'Intended Audience :: Telecom Log Debuggers',

            # License
            'License :: OSI Approved :: MIT License',

            # Package Language
            'Natural Language :: English',

            # Python Verison
            'Programming Language :: Python :: 2.x',
            'Programming Language :: Python :: 3.x',
        ]
)