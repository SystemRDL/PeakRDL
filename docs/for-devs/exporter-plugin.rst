.. _exporter-plugin:

Defining your own Exporter
==========================

The PeakRDL command line tool can be extended with your own custom exporter
subcommands. This page describes how you can implement an extension that PeakRDL
will automatically discover, and make available in the command line interface.

Any exporter you make shall be an installable Python package. See
`Python's packaging guide <https://packaging.python.org>`_ for more details on
how to do this.


Exporter Implementation
-----------------------

First, implement your exporter function or class. It is good practice to implement
this separately from the descriptor class below so that you provide good separation
of concepts. This will allow others to use your exporter on its own, outside the
context of the PeakRDL command line tool.

See the `SystemRDL compiler reference for some examples <https://systemrdl-compiler.readthedocs.io/en/stable/examples/print_hierarchy.html>`_.


Descriptor Class
----------------

The descriptor class is how you describe your exporter to PeakRDL. This class
includes help text, defines your command line arguments, and provides a function
that implements your custom export operation.
This class should only be a simple wrapper that calls your exporter
implementation.

For consistency, it is recommended to define this descriptor class in a file
named ``__peakrdl__.py`` at the root of your package.

Members of this descriptor class are as follows:

.. data:: short_desc

    A brief one-line description of your exporter command.


.. data:: long_desc

    (optional) A longer description.


.. data:: generates_output_file

    (optional) Defaults to ``True``, which implicitly defines a required command
    line argument ``-o OUTPUT_PATH``. The result of this is available later in
    the ``do_export()`` function via ``options.output``.

    Set this to ``False`` if your exporter does not write any output files.


.. function:: add_exporter_arguments(self, arg_group)

    (optional) Use this function to define additional command line arguments by
    using the ``arg_group.add_argument()`` method.
    See Python's `argparse module <https://docs.python.org/3/library/argparse.html#the-add-argument-method>`_
    for more details on how to use this.

    :param arg_group: argparse ArgumentParser object


.. function:: do_export(self, top_node, options)

    Defines the implementation of your exporter.

    :param top_node: SystemRDL AddrmapNode object representing the top of the design to be exported
    :param options: argparse Namespace object containing all the command line argument values


Below is a template you can use as a starting point:

.. code-block:: python

    class MyExporterDescriptor:
        short_desc = "..."
        long_desc = "..."

        def add_exporter_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
            pass

        def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
            raise NotImplementedError


For a complete example, see `PeakRDL-ipxact's __peakrdl__.py file <https://github.com/SystemRDL/PeakRDL-ipxact/blob/main/src/peakrdl_ipxact/__peakrdl__.py>`_.



Entry Point
-----------

The PeakRDL command line tool automatically discovers exporters by scanning the
entry points that installed packages advertise.
The example below shows how you would provide an entry point linkage to your
exporter's descriptor class inside your package's ``setup.py``:

.. code-block:: python
    :emphasize-lines: 7-11

    import setuptools

    setuptools.setup(
        name="my_package",
        packages=["my_package"],
        # ...
        entry_points = {
            "peakrdl.exporters": [
                'my-exporter = my_package.__peakrdl__:MyExporterDescriptor'
            ]
        }
    )

* ``my_package``: The name of your installable Python module
* ``peakrdl.exporters``: This is the namespace that PeakRDL will search. Any
  exporters you create must be enclosed in this namespace in order to be
  discovered.
* ``my_package.__peakrdl__:MyExporterDescriptor``: This is the import path that
  points to your descriptor class definition
* ``my-exporter``: The lefthand side of the assignment is your exporter's
  subcommand name. This text is what is used in the command line interface.

For a complete example, see `PeakRDL-ipxact's setup.py file <https://github.com/SystemRDL/PeakRDL-ipxact/blob/main/setup.py>`_.
