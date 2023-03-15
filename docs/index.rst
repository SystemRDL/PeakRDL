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

.. toctree::
    :hidden:
    :caption: Additional Exporter Docs

    regblock <https://peakrdl-regblock.readthedocs.io/en/latest>
    ip-xact <https://peakrdl-ipxact.readthedocs.io/en/latest/exporter.html>

.. toctree::
    :hidden:
    :caption: For Developers

    for-devs/exporter-plugin
    for-devs/importer-plugin
    for-devs/descriptors
    for-devs/cfg_schema
