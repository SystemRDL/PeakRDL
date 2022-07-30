from typing import TYPE_CHECKING, List, Dict, Any
import re
import os

from systemrdl import RDLCompiler, AddrmapNode
from systemrdl.messages import FileSourceRef

if TYPE_CHECKING:
    import argparse
    from .importer import Importer


def add_rdl_compile_arguments(parser: 'argparse._ActionsContainer') -> None:
    parser.add_argument(
        "input_files",
        metavar="FILE",
        nargs="+",
        help="One or more input files"
    )
    parser.add_argument(
        "-I",
        dest="incdirs",
        metavar="INCDIR",
        action="append",
        help='Search directory for files included with `include "filename"',
    )


def add_importer_arguments(parser: 'argparse._ActionsContainer', importers: 'List[Importer]') -> None:
    for importer in importers:
        importer_arg_group = parser.add_argument_group(f"{importer.name} importer args")
        importer.add_importer_arguments(importer_arg_group)


def add_elaborate_arguments(parser: 'argparse._ActionsContainer') -> None:
    parser.add_argument(
        "-t", "--top",
        dest="top_def_name",
        metavar="TOP",
        default=None,
        help="Explicitly choose which addrmap  in the root namespace will be the "
                "top-level component. If unset, The last addrmap defined will be chosen"
    )
    parser.add_argument(
        "--rename",
        dest="inst_name",
        default=None,
        help="Overrides the top-component's instantiated name. By default, the "
                "instantiated name is the same as the component's type name"
    )
    parser.add_argument(
        "-P",
        dest="parameters",
        metavar="PARAMETER=VALUE",
        action="append",
        default=[],
        help='Specify value for a top-level SystemRDL parameter',
    )


def parse_parameters(rdlc: RDLCompiler, parameter_options: List[str]) -> Dict[str, Any]:
    parameters = {}
    for raw_param in parameter_options:
        m = re.fullmatch(r"(\w+)=(.+)", raw_param)
        if not m:
            rdlc.msg.fatal(f"Invalid parameter argument: {raw_param}")

        p_name = m.group(1)
        try:
            p_value = rdlc.eval(m.group(2))
        except ValueError:
            rdlc.msg.fatal(f"Unable to parse value '{m.group(2)}' for parameter '{p_name}'")
        parameters[p_name] = p_value

    return parameters


def process_input(rdlc: RDLCompiler, importers: 'List[Importer]', input_files: List[str], options: 'argparse.Namespace') -> None:
    for file in input_files:
        if not os.path.exists(file):
            rdlc.msg.fatal(f"Input file does not exist: {file}")

        ext = os.path.splitext(file)[1].strip(".")
        if ext == "rdl":
            # Is SystemRDL file
            rdlc.compile_file(
                file,
                incl_search_paths=options.incdirs,
            )
        else:
            # Is foreign input file.

            # Search which importer to use by extension first
            importer_candidates = [] # type: List[Importer]
            for importer in importers:
                if ext in importer.file_extensions:
                    importer_candidates.append(importer)

            # Do 2nd pass if needed
            importer = None
            if len(importer_candidates) == 1:
                importer = importer_candidates[0]
            elif len(importer_candidates) > 1:
                # ambiguous which importer to use
                # Do 2nd pass compatibility check
                for importer_candidate in importer_candidates:
                    if importer_candidate.is_compatible(file):
                        importer = importer_candidate
                        break

            if not importer:
                rdlc.msg.fatal(
                    "Unknown file type. Could not find any importers capable of reading this file.",
                    FileSourceRef(file)
                )

            importer.do_import(rdlc, options, file)


def elaborate(rdlc: RDLCompiler, parameters: Dict[str, Any], options: 'argparse.Namespace') -> AddrmapNode:
    try:
        root = rdlc.elaborate(
            top_def_name=options.top_def_name,
            inst_name=options.inst_name,
            parameters=parameters
        )
    except (ValueError, TypeError) as e:
        # Parameter issues raise ValueError or TypeError
        # TODO: Fix exception types once they become specialized in the compiler
        rdlc.msg.fatal(e.args[0])

    return root.top
