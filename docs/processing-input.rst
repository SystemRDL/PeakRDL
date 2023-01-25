Processing Input
================

File order and linking
----------------------

The PeakRDL command line tool is capable of processing multiple input files and
linking them together. Component declarations are added to a common namespace
that is shared across files, allowing components to be instantiated in another file.

Since PeakRDL processes and links files in-order, it is important to provide the
list of files in the correct sequence - dependencies first, top-level last:

.. code-block:: bash

    peakrdl <command> subblock1.rdl subblock2.rdl top.rdl


Top-level elaboration
---------------------
Unless specified otherwise, PeakRDL will elaborate the last addrmap component
that was declared in the root namespace.

For example, given the following input file:

.. code-block:: systemrdl
    :name: example.rdl

    addrmap common {
        reg {
            field {} spam_y;
        } spam_x;
    };

    addrmap foo {
        common block_a;
        common block_b;
    };

    addrmap bar {
        common block_x;
        common block_y;
    };

By default, PeakRDL will elaborate ``bar`` as the top-level node, since it is last:

.. code-block:: bash

    $ peakrdl dump example.rdl
    0x0-0x3: bar.block_x.spam_x
    0x4-0x7: bar.block_y.spam_x

Or you can explicitly choose an alternative addrmap to elaborate using the ``--top`` flag:

.. code-block:: bash

    $ peakrdl dump example.rdl --top foo
    0x0-0x3: foo.block_a.spam_x
    0x4-0x7: foo.block_b.spam_x

If you are not sure what targets are available as top-levels, you can list all
that are available using the ``globals`` command:

.. code-block:: bash

    $ peakrdl globals example.rdl
    common
    foo
    bar



Supported Input Formats
-----------------------

PeakRDL can support intermixing various input formats.


SystemRDL 2.0
^^^^^^^^^^^^^

SystemRDL is the primary register model source format for PeakRDL.

For a full description of the register description language standard, see
`Accellera's SystemRDL 2.0 specification <http://accellera.org/downloads/standards/systemrdl>`_.

Internally, PeakRDL uses the `systemrdl-compiler <https://systemrdl-compiler.readthedocs.io>`_ package
to interpret and elaborate RDL input.


IP-XACT XML
^^^^^^^^^^^

PeakRDL is capable of importing IP-XACT XML files. These are converted into SystemRDL semantics by the importer.
For more details on how the importer works, see the `PeakRDL-ipxact documentation <https://peakrdl-ipxact.readthedocs.io/en/latest/importer.html>`_.

For more details on the IP-XACT format, see `Accellera's standards page <https://www.accellera.org/downloads/standards/ip-xact>`_



Your custom importer extension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PeakRDL's capabilities can be extended with your own custom importer plugin.
See more details here: :ref:`importer-plugin`
