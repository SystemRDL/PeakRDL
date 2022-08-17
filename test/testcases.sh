#!/bin/bash

set -e

this_dir="$( cd "$(dirname "$0")" ; pwd -P )"
cd $this_dir

mkdir -p test.out

src=../examples/atxmega_spi.rdl

peakrdl -h
peakrdl dump $src
peakrdl globals $src
peakrdl uvm $src -o test.out/uvm.pkg
mkdir -p test.out/regblock
peakrdl regblock $src -o test.out/regblock
peakrdl ip-xact $src -o test.out/ipxact.xml
mkdir -p test.out/html
peakrdl html $src -o test.out/html
