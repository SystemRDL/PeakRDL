import os
import setuptools

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()


with open(os.path.join("src/peakrdl", "__about__.py"), "r", encoding='utf-8') as f:
    v_dict = {}
    exec(f.read(), v_dict)
    version = v_dict['__version__']

setuptools.setup(
    name="peakrdl",
    version=version,
    author="Alex Mykyta",
    author_email="amykyta3@github.com",
    description="Command-line tool for control/status register automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SystemRDL/PeakRDL",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points = {
        "console_scripts": ['peakrdl = peakrdl.main:main']
    },
    python_requires='>=3.6',
    install_requires=[
        "systemrdl-compiler >= 1.26.0, < 2",
        "peakrdl-html >= 2.10.1, < 3",
        "peakrdl-ipxact >= 3.4.1, < 4",
        "peakrdl-regblock >= 0.18.0",
        "peakrdl-systemrdl >= 0.3.0",
        "peakrdl-uvm >= 2.3.0, < 3",
        "tomli;python_version<'3.11'"
    ],
    classifiers=(
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ),
    project_urls={
        "Documentation": "https://peakrdl.readthedocs.io",
        "Source": "https://github.com/SystemRDL/PeakRDL",
        "Tracker": "https://github.com/SystemRDL/PeakRDL/issues",
        "Changelog": "https://github.com/SystemRDL/PeakRDL/releases",
    },
)
