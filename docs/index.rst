Introduction
============

PeakRDL is a free and open-source control & status register (CSR) generator
toolchain. This project provides a command-line tool that unifies many aspects
of register automation such as generating Verilog CSR RTL, compiling a
C register abstraction layer, and many more. PeakRDL is centered around the
SystemRDL register description language, but is also capable of working with
other CSR specifications like IP-XACT.

This tool can:

* Process SystemRDL 2.0 register descriptions.
* Generate synthesizable SystemVerilog RTL register blocks.
* Generate a C register abstraction header for software.
* Import & export IP-XACT XML.
* Create rich and dynamic HTML documentation.
* Build a UVM register model abstraction layer.
* Be extended by :ref:`exporter-plugin` plugin.
* ... or use one of the many :ref:`community-plugins`



Installing
----------

Install from `PyPi`_ using pip

.. code-block:: bash

    python3 -m pip install peakrdl

.. _PyPi: https://pypi.org/project/peakrdl



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
    gallery
    systemrdl-tutorial
    processing-input
    configuring
    licensing
    community

.. toctree::
    :hidden:
    :caption: Additional Exporter Docs

    regblock <https://peakrdl-regblock.readthedocs.io>
    c-header <https://peakrdl-cheader.readthedocs.io>
    ip-xact <https://peakrdl-ipxact.readthedocs.io/en/latest/exporter.html>

.. toctree::
    :hidden:
    :caption: For Developers

    for-devs/exporter-plugin
    for-devs/importer-plugin
    for-devs/descriptors
    for-devs/cfg_schema
