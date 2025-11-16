.. _importer-plugin:

Defining your own Importer
==========================

Importers allow you to extend the types of files that the PeakRDL tool is able
to interpret. This page describes how you can implement an extension that PeakRDL
will automatically discover and use when interpreting its input files.


Importer Implementation
-----------------------

First, implement your importer class. It is good practice to implement
this separately from the descriptor class below so that you provide good separation
of concepts. This will allow others to use your importer on its own, outside the
context of the PeakRDL command line tool.

See the `SystemRDL compiler reference for an example <https://systemrdl-compiler.readthedocs.io/en/stable/examples/json_importer.html>`_.


Plugin Descriptor Class
-----------------------

The plugin descriptor class is how you describe your importer to PeakRDL.
This class should only be a simple wrapper that calls your importer
implementation, and shall be extended from :class:`~peakrdl.plugins.importer.ImporterPlugin`

Below is a template you can use as a starting point:

.. code-block:: python

    from typing import TYPE_CHECKING

    from peakrdl.plugins.importer import ImporterPlugin

    if TYPE_CHECKING:
        import argparse
    from systemrdl import RDLCompiler

    class MyImporterDescriptor(ImporterPlugin):
        file_extensions = ["yaml", "yml"]

        def is_compatible(self, path: str) -> bool:
            raise NotImplementedError

        def add_importer_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
            pass

        def do_import(self, rdlc: 'RDLCompiler', options: 'argparse.Namespace', path: str):
            raise NotImplementedError

For more advanced plugins, see the full :class:`~peakrdl.plugins.importer.ImporterPlugin`
reference.

For a complete example, see `PeakRDL-ipxact's __peakrdl__.py file <https://github.com/SystemRDL/PeakRDL-ipxact/blob/main/src/peakrdl_ipxact/__peakrdl__.py>`_.


Plugin Discovery
----------------

There are two ways PeakRDL can discover your plugin.

Via Entry Point
^^^^^^^^^^^^^^^

Entry points are the recommended way to advertise PeakRDL plugins, especially if
you plan to share your plugin more broadly as a pip-installable package.

The PeakRDL command line tool automatically discovers importers by scanning the
entry points that installed packages advertise.
See
`Python's packaging guide <https://packaging.python.org>`_ for more details on
how to make an installable package.

For consistency, it is recommended to define your plugin descriptor class in a
file named ``__peakrdl__.py`` at the root of your package.

The example below shows how you would provide an entry point linkage to your
importer's descriptor class inside your package's ``pyproject.toml``:

.. code-block:: toml

    [project.entry-points."peakrdl.importers"]
    my-importer = "my_package.__peakrdl__:MyImporterDescriptor"


* ``my_package``: The name of your installable Python module
* ``peakrdl.importers``: This is the namespace that PeakRDL will search. Any
  importers you create must be enclosed in this namespace in order to be
  discovered.
* ``my_package.__peakrdl__:MyImporterDescriptor``: This is the import path that
  points to your descriptor class definition



Via the PeakRDL configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An alternative method that avoids having to make your own pip-installable
package is to specify the plugin import entry point via the PeakRDL
configuration file. This is useful for smaller ad-hoc plugins or experimental
extensions.

For example, if your plugin descriptor was defined in a Python file located in
``/opt/my_peakrdl_plugins/my_importer.py``, the following configuration would
instruct PeakRDL to load it:

.. code-block:: toml

    [peakrdl]

    # Paths for Python to search for importable modules
    python_search_paths = [
        "/opt/my_peakrdl_plugins"
    ]

    # Define entry-point spec for the exporter
    plugins.importers.my-importer = "my_importer:MyImporterDescriptor"
