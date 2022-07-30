.. _importer-plugin:

Defining your own Importer
==========================

Importers allow you to extend the types of files that the PeakRDL tool is able
to interpret. This page describes how you can implement an extension that PeakRDL
will automatically discover and use when interpreting its input files.

Similar to an exporter, any importer you make shall be an installable Python package. See
`Python's packaging guide <https://packaging.python.org>`_ for more details on
how to do this.


Importer Implementation
-----------------------

First, implement your importer class. It is good practice to implement
this separately from the descriptor class below so that you provide good separation
of concepts. This will allow others to use your exporter on its own, outside the
context of the PeakRDL command line tool.

See the `SystemRDL compiler reference for an example <https://systemrdl-compiler.readthedocs.io/en/stable/examples/json_importer.html>`_.


Descriptor Class
----------------

For consistency, it is recommended to define this descriptor class in a file
named ``__peakrdl__.py`` at the root of your package.

Members of this descriptor class are as follows:

.. data:: file_extensions

    A list of one or more file extensions your importer expects to support.
    A file's extension is used as a rough first-pass method to identify which
    importer is appropriate for a given file type.

.. function:: is_compatible(self, path)

    This function is used to further determine if this importer is capable of
    processing the given input file.
    It is recommended to open the file, and perform a low-cost scan of the
    contents to quickly determine if the file's format appears to be compatible
    with this importer.

    :param path: Path to the input file

.. function:: add_importer_arguments(self, arg_group)

    (optional) Use this function to define additional command line arguments that
    are relevant to this importer via the ``arg_group.add_argument()`` method.
    See Python's `argparse module <https://docs.python.org/3/library/argparse.html#the-add-argument-method>`_
    for more details on how to use this.

    :param arg_group: argparse ArgumentParser object

.. function:: do_import(self, rdlc, options, path)

    Defines the implementation of your importer.

    :param rdlc: Reference to the SystemRDL ``RDLCompiler`` object.
    :param options: argparse Namespace object containing all the command line argument values
    :param path: Path to the input file


Below is a template you can use as a starting point:

.. code-block:: python

    class MyImporterDescriptor:
        file_extensions = ["yaml", "yml"]

        def is_compatible(self, path: str) -> bool:
            raise NotImplementedError

        def add_importer_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
            pass

        def do_import(self, rdlc: 'RDLCompiler', options: 'argparse.Namespace', path: str):
            raise NotImplementedError

For a complete example, see `PeakRDL-ipxact's __peakrdl__.py file <https://github.com/SystemRDL/PeakRDL-ipxact/blob/main/src/peakrdl_ipxact/__peakrdl__.py>`_.



Entry Point
-----------

The PeakRDL command line tool automatically discovers importers by scanning the
entry points that installed packages advertise.
The example below shows how you would provide an entry point linkage to your
importer's descriptor class inside your package's ``setup.py``:

.. code-block:: python
    :emphasize-lines: 7-11

    import setuptools

    setuptools.setup(
        name="my_package",
        packages=["my_package"],
        # ...
        entry_points = {
            "peakrdl.importers": [
                'my-importer = my_package.__peakrdl__:MyImporterDescriptor'
            ]
        }
    )

* ``my_package``: The name of your installable Python module
* ``peakrdl.importers``: This is the namespace that PeakRDL will search. Any
  importers you create must be enclosed in this namespace in order to be
  discovered.
* ``my_package.__peakrdl__:MyImporterDescriptor``: This is the import path that
  points to your descriptor class definition

For a complete example, see `PeakRDL-ipxact's setup.py file <https://github.com/SystemRDL/PeakRDL-ipxact/blob/main/setup.py>`_.
