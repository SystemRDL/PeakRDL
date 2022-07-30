from typing import TYPE_CHECKING
import math

from systemrdl import RDLListener, RDLWalker
from systemrdl.node import AddrmapNode, RegNode

from ..subcommand import ExporterSubcommand

if TYPE_CHECKING:
    import argparse


class DumpListener(RDLListener):
    def __init__(self, hex_digits:int, unroll: bool) -> None:
        self.hex_digits = hex_digits
        self.unroll = unroll

    def enter_Reg(self, node: RegNode) -> None:
        if self.unroll:
            addr = node.absolute_address
            size = node.size
        else:
            addr = node.raw_absolute_address
            size = node.total_size

        print(
            f"0x{addr:0{self.hex_digits}x}-0x{addr+size-1:0{self.hex_digits}x}:",
            node.get_path(empty_array_suffix="[{dim:d}]")
        )


class Dump(ExporterSubcommand):
    name = "dump"
    short_desc = "print register model contents to stdout"
    generates_output_file = False

    def add_exporter_arguments(self, arg_group: 'argparse._ActionsContainer') -> None:
        super().add_exporter_arguments(arg_group)

        arg_group.add_argument(
            "-u", "--unroll",
            default=False,
            action="store_true",
            help="Unroll arrays"
        )


    def do_export(self, top_node: AddrmapNode, options: 'argparse.Namespace') -> None:
        hex_digits = math.ceil(top_node.total_size.bit_length() / 4)
        walker = RDLWalker(unroll=options.unroll)
        listener = DumpListener(hex_digits, options.unroll)
        walker.walk(top_node, listener)
