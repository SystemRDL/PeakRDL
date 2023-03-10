.. _cfg_schema:

Configuration Schema
====================

In order to simplify the usage of the PeakRDL configuration TOML, a simple
configuration validation and data extraction schema is provided.

This provides an intuitive way for plugin developers to define what TOML
configuration options exist, as well as their expected datatypes.


Example
-------

Consider an exporter plugin that wants to define some additional configuration
options for the PeakRDL TOML as follows:

.. code-block:: toml

    [my-exporter]
    # Expects an integer
    max_depth = 1234

    # Expects a list of strings
    prefixes = ["my_prefix", "other_prefix"]

    # Expects a file path
    extra_file_path = "../path/to/thing.txt"


The expected datatype structure of these options can be defined in the descriptor
class as follows:

.. code-block:: python
    :emphasize-lines: 6-10

    from peakrdl.plugins.exporter import ExporterSubcommandPlugin
    from peakrdl.config import schema

    class MyExporter(ExporterSubcommandPlugin):

        cfg_schema = {
            "max_depth": schema.Integer(),
            "prefixes": [schema.String()],
            "extra_file_path": schema.FilePath(),
        }

Then, when performing the export in the ``do_export()`` method, the values of
these options can be queried as follows:

.. code-block:: python

    def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
        self.cfg['max_depth']
        self.cfg['prefixes']
        self.cfg['extra_file_path']


Lists and Mappings
------------------
When defining your configuration schema, lists and mapping schemas can be defined
using a shorthand notation.

A list of uniform element types can be defined by enclosing the element's schema
in a list:

.. code-block:: python

    # Defines a schema for a list of integers
    [schema.Integer()]

A mapping of fixed key:value pairs can be defined as a dictionary that describes
each mapping member:

.. code-block:: python

    {
        "an_integer": schema.Integer(),
        "a_string": schema.String(),
    }

A mapping that accepts any user-defined keys with a uniform value:

.. code-block:: python

    {"*": schema.Integer()}


Default values
--------------

After extraction, if a configuration value is not explicitly specified by the
user, the resulting configuration data structure will contain the following:

* Fixed mappings will contain all the expected keys. Values will contain their
  default value as specified by this section.
* A mapping with user-defined keys will default to be empty.
* A list will default to be empty
* All other values will default to ``None``


Schema Object Reference
-----------------------

Base Datatypes
^^^^^^^^^^^^^^

.. autoclass:: peakrdl.config.schema.String
.. autoclass:: peakrdl.config.schema.Integer
.. autoclass:: peakrdl.config.schema.Float
.. autoclass:: peakrdl.config.schema.Boolean
.. autoclass:: peakrdl.config.schema.DateTime
.. autoclass:: peakrdl.config.schema.Date
.. autoclass:: peakrdl.config.schema.Time

Paths
^^^^^
.. autoclass:: peakrdl.config.schema.Path
.. autoclass:: peakrdl.config.schema.FilePath
.. autoclass:: peakrdl.config.schema.DirectoryPath

Python Objects
^^^^^^^^^^^^^^
.. autoclass:: peakrdl.config.schema.PythonObjectImport
