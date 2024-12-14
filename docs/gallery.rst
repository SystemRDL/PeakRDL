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


Generate C headers for software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    peakrdl c-header atxmega_spi.rdl -o atxmega_spi.h

    # .. Or with bit-fields
    peakrdl c-header atxmega_spi.rdl -o atxmega_spi_bf.h --bitfields ltoh


Input: `atxmega_spi.rdl <https://github.com/SystemRDL/PeakRDL/tree/main/examples/atxmega_spi.rdl>`_

Result: `atxmega_spi.h <https://github.com/SystemRDL/PeakRDL/blob/main/examples/atxmega_spi.h>`_ &
`atxmega_spi_bf.h <https://github.com/SystemRDL/PeakRDL/blob/main/examples/atxmega_spi_bf.h>`_


Convert to IP-XACT XML
^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: bash

    peakrdl ip-xact atxmega_spi.rdl -o atxmega_spi.xml

Input: `atxmega_spi.rdl <https://github.com/SystemRDL/PeakRDL/tree/main/examples/atxmega_spi.rdl>`_

Result: `atxmega_spi.xml <https://github.com/SystemRDL/PeakRDL/blob/main/examples/atxmega_spi.xml>`_

For more details, see the full `PeakRDL-ipxact documentation <https://peakrdl-ipxact.readthedocs.io/en/latest/exporter.html>`_.


Convert other formats to SystemRDL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Convert IP-XACT to SystemRDL
    peakrdl systemrdl atxmega_spi.xml -o atxmega_spi.rdl


Provided by `PeakRDL-systemrdl <https://github.com/SystemRDL/PeakRDL-systemrdl>`_.


Run your own custom command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    peakrdl YOUR-COMMAND-HERE atxmega_spi.rdl ...

PeakRDL can be extended with additional user-defined commands.
See more details here: :ref:`exporter-plugin`

Or, check out the various :ref:`community-plugins` already available.
