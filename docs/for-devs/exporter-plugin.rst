.. _exporter-plugin:

Defining your own Exporter
==========================

The PeakRDL command line tool can be extended with your own custom exporter
subcommands. This page describes how you can implement an extension that PeakRDL
will automatically discover, and make available in the command line interface.


Exporter Implementation
-----------------------

First, implement your exporter function or class. It is good practice to implement
this separately from the descriptor class below so that you provide good separation
of concepts. This will allow others to use your exporter on its own, outside the
context of the PeakRDL command line tool.

See the `SystemRDL compiler reference for some examples <https://systemrdl-compiler.readthedocs.io/en/stable/examples/print_hierarchy.html>`_.


Plugin Descriptor Class
-----------------------

The plugin descriptor class is how you describe your exporter to PeakRDL. This
class includes help text, defines your command line arguments, and provides a
function that implements your custom export operation.
This class should only be a simple wrapper that calls your exporter
implementation, and shall be extended from :class:`~peakrdl.plugins.exporter.ExporterSubcommandPlugin`

Below is a template you can use as a starting point:

.. code-block:: python

    from typing import TYPE_CHECKING

    from peakrdl.plugins.exporter import ExporterSubcommandPlugin

    if TYPE_CHECKING:
        import argparse
        from systemrdl.node import AddrmapNode

    class MyExporterDescriptor(ExporterSubcommandPlugin):
        short_desc = "..."
        long_desc = "..."

        def add_exporter_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
            pass

        def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
            raise NotImplementedError

For more advanced plugins, see the full :class:`~peakrdl.plugins.exporter.ExporterSubcommandPlugin`
reference.

For a complete example, see `PeakRDL-ipxact's __peakrdl__.py file <https://github.com/SystemRDL/PeakRDL-ipxact/blob/main/src/peakrdl_ipxact/__peakrdl__.py>`_.


Plugin Discovery
----------------

There are two ways PeakRDL can discover your plugin.

Via Entry Point
^^^^^^^^^^^^^^^

The PeakRDL command line tool automatically discovers exporters by scanning the
entry points that installed packages advertise.
See
`Python's packaging guide <https://packaging.python.org>`_ for more details on
how to make an installable package.

For consistency, it is recommended to define your plugin descriptor class in a
file named ``__peakrdl__.py`` at the root of your package.

The example below shows how you would provide an entry point linkage to your
exporter's descriptor class inside your package's ``pyproject.toml``:

.. code-block:: toml

    [project.entry-points."peakrdl.exporters"]
    my-exporter = "my_package.__peakrdl__:MyExporterDescriptor"


* ``my_package``: The name of your installable Python module
* ``peakrdl.exporters``: This is the namespace that PeakRDL will search. Any
  exporters you create must be enclosed in this namespace in order to be
  discovered.
* ``my_package.__peakrdl__:MyExporterDescriptor``: This is the import path that
  points to your descriptor class definition
* ``my-exporter``: The lefthand side of the assignment is your exporter's
  subcommand name. This text is what is used in the command line interface.

For a complete example, see `PeakRDL-cheader's pyproject.toml file <https://github.com/SystemRDL/PeakRDL-cheader/blob/main/pyproject.toml>`_.


Via the PeakRDL configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An alternative method that avoids having to make your own pip-installable
package is to specify the plugin import entry point via the PeakRDL
configuration file.

For example, if your plugin descriptor was defined in a Python file located in
``/opt/my_peakrdl_plugins/my_exporter.py``, the following configuration would
instruct PeakRDL to load it:

.. code-block:: toml

    [peakrdl]

    # Paths for Python to search for importable modules
    python_search_paths = [
        "/opt/my_peakrdl_plugins"
    ]

    # Define entry-point spec for the exporter
    plugins.exporters.my-exporter = "my_exporter:MyExporterDescriptor"
