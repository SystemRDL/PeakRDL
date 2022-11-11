Introduction
============

PeakRDL is a free and open-source control & status register (CSR) toolchain.
This projects provides a command-line tool that unifies many aspects of register
automation centered around the SystemRDL register description language.

This tool can:

* Process SystemRDL 2.0 register descriptions.
* Import & export IP-XACT XML.
* Generate synthesizable SystemVerilog RTL register blocks.
* Create rich and dynamic HTML documentation.
* Build a UVM register model abstraction layer.
* ... or extended this tool with your own plugins

.. warning::

    The PeakRDL command line tool is still in pre-production (v0.x version numbers).
    During this time, I may decide to refactor things which could break compatibility.


Installing
----------

Install from `PyPi`_ using pip

.. code-block:: bash

    python3 -m pip install peakrdl

.. _PyPi: https://pypi.org/project/peakrdl


Gallery of Examples
-------------------

These are all very simple examples of what you can do with PeakRDL but be aware that
you can do far more powerful things.

For more details, see the individual command's ``--help`` flag.

.. code-block:: bash

    # For general help
    peakrdl --help

    # For help about a specific subcommand:
    peakrdl <subcommand> --help


Generate syntesizable SystemVerilog RTL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    peakrdl regblock atxmega_spi.rdl -o regblock/ --cpuif apb3-flat

Input: `atxmega_spi.rdl <https://github.com/SystemRDL/PeakRDL/tree/main/examples/atxmega_spi.rdl>`_

Result: `regblock/ <https://github.com/SystemRDL/PeakRDL/tree/main/examples/regblock>`_

For more details, see the full `PeakRDL-regblock documentation <https://peakrdl-regblock.readthedocs.io>`_.


Produce dynamic HTML documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    peakrdl html turboencabulator.rdl -o html_dir/

Input: `turboencabulator.rdl <https://github.com/SystemRDL/PeakRDL-html/blob/main/example/turboencabulator.rdl>`_

Result: `HTML register reference <https://systemrdl.github.io/PeakRDL-html>`_


Create a UVM Register Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    peakrdl uvm atxmega_spi.rdl -o atxmega_spi_uvm_pkg.sv

Input: `atxmega_spi.rdl <https://github.com/SystemRDL/PeakRDL/tree/main/examples/atxmega_spi.rdl>`_

Result: `atxmega_uvm_pkg.sv <https://github.com/SystemRDL/PeakRDL/blob/main/examples/atxmega_spi_uvm_pkg.sv>`_


Convert to IP-XACT XML
^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    peakrdl ip-xact atxmega_spi.rdl -o atxmega_spi.xml

Input: `atxmega_spi.rdl <https://github.com/SystemRDL/PeakRDL/tree/main/examples/atxmega_spi.rdl>`_

Result: `atxmega_spi.xml <https://github.com/SystemRDL/PeakRDL/blob/main/examples/atxmega_spi.xml>`_

For more details, see the full `PeakRDL-ipxact documentation <https://peakrdl-ipxact.readthedocs.io/en/latest/exporter.html>`_.


Run your own custom command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    peakrdl YOUR-COMMAND-HERE atxmega_spi.rdl ...

PeakRDL can be extended with additional user-defined commands.
See more details here: :ref:`exporter-plugin`


Links
-----

- `Source repository <https://github.com/SystemRDL/PeakRDL>`_
- `Release Notes <https://github.com/SystemRDL/PeakRDL/releases>`_
- `Issue tracker <https://github.com/SystemRDL/PeakRDL/issues>`_
- `PyPi <https://pypi.org/project/peakrdl>`_
- `SystemRDL Specification <http://accellera.org/downloads/standards/systemrdl>`_


.. toctree::
    :hidden:

    self
    systemrdl-tutorial
    processing-input
    licensing

.. toctree::
    :hidden:
    :caption: For Developers

    for-devs/exporter-plugin
    for-devs/importer-plugin
