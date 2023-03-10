Configuring PeakRDL
===================

Additional configuration options can be provided to PeakRDL and its plugins via
a `TOML <https://toml.io>`_ file. These configuration options are
in addition to runtime command-line options and are intended to be static
settings that are specific to your development environment.


Specifying a configuration file
-------------------------------

The PeakRDL configuration file can be explicitly specified using the
``--peakrdl-cfg`` option. Otherwise, Peakrdl searches for a configuration file
in the following order, and uses the first one it finds:

1. ``peakrdl.toml`` in the current working directory
2. ``.peakrdl.toml`` in the current working directory
3. The file named by environment variable ``PEAKRDL_CFG``
4. ``.peakrdl.toml`` in your home directory
5. ``.config/peakrdl.toml`` in your home directory
6. In ``/etc/peakrdl.toml``


PeakRDL configuration options
-----------------------------

Options specific to the PeakRDL core are defined under the ``[peakrdl]`` TOML heading.

.. data:: python_search_paths

    Provide additional search paths for Python to use to discover importable modules.
    Paths can be absolute, or relative to the enclosing config file.

.. data:: plugins.importers

    Mapping of additional importer plugins to load.
    The mapping's key indicates the importer's name.
    The value is a string that describes the import path and importer class to
    load.

    For example:

    .. code-block:: toml

        [peakrdl]
        plugins.importers.my-importer-name = "my_importer_module:MyImporterDescriptorClass"


.. data:: plugins.exporters

    Mapping of additional exporter plugins to load.
    The mapping key indicates the exporter's subcommand name.
    The value is a string that describes the import path and exporter class to
    load.

    For example:

    .. code-block:: toml

        [peakrdl]
        plugins.exporters.my-exporter-name = "my_exporter_module:MyExporterDescriptorClass"



Plugin-specific configuration options
-------------------------------------

Importers and exporters may define their own configuration options as necessary.
Their configuration options are defined within their own heading of the corresponding name.
For example:

.. code-block:: toml

    [html]
    user_template_dir = "../path/to/html_templates"
    extra_doc_properties = ["hw", "my_udp"]

See the plugin-specific reference documents for more details onhow they can be configured.
