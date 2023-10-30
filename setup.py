from setuptools import setup, find_packages
import pathlib

requirements = [
    "flask",
    "flask-socketio", # ?
    "flask-sock",
    "InquirerPy",
    "rich",
    "typer",
]

setup(
    name='neca',
    version='2.1.8',
    description='ECA: Event Condition Action ',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/NiekAukes/eca2',
    author='Niek Aukes',
    author_email="niek.aukes@gmail.com",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    
    packages=find_packages(),	
    python_requires=">=3.7, <4",
    # read from requirements.txt
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "neca": ["templates/*", "tutorials/*", "demos/*", "statics/*"],
    },
    
    entry_points={
        "console_scripts": [
            "neca=neca.__main__:cli",
        ]
    },

    project_urls={  # Optional
        "Bug Reports": "https://github.com/NiekAukes/eca2/issues",
        "Source": "https://github.com/NiekAukes/eca2"
    }
)
