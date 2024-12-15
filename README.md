[![Documentation Status](https://readthedocs.org/projects/peakrdl/badge/?version=latest)](http://peakrdl.readthedocs.io)
[![build](https://github.com/SystemRDL/PeakRDL/workflows/build/badge.svg)](https://github.com/SystemRDL/PeakRDL/actions?query=workflow%3Abuild+branch%3Amain)
[![Coverage Status](https://coveralls.io/repos/github/SystemRDL/PeakRDL/badge.svg?branch=main)](https://coveralls.io/github/SystemRDL/PeakRDL?branch=main)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/peakrdl.svg)](https://pypi.org/project/peakrdl)

# PeakRDL

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
* Extend this tool with your own plugin.
* ... or use one of the many [community plugins](https://peakrdl.readthedocs.io/en/latest/community.html)


## Documentation
See the [PeakRDL Documentation](http://peakrdl.readthedocs.io) for more details.
