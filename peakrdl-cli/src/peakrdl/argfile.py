import sys
import os
import shlex
import re
from typing import List, Optional, Set, Match

def expand_tokens(argv: List[str]) -> List[str]:
    """
    Expand environment variables in args
    """
    pattern = re.compile(r"\$(\w+|\{[^}]*\})")
    def repl(m: Match) -> str:
        k = m.group(1)
        if k.startswith("{") and k.endswith("}"):
            k = k[1:-1]

        v = os.environ.get(k, m.group(0))
        return v

    return [pattern.sub(repl, arg) for arg in argv]


def parse_argfile(path: str) -> List[str]:
    if not os.path.exists(path):
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding='utf-8') as f:
        args = shlex.split(f.read(), comments=True)
        args = expand_tokens(args)
        return args


def expand_argfile(argv: List[str], _pathlist: Optional[Set[str]] = None) -> List[str]:
    if _pathlist is None:
        _pathlist = set()

    new_argv = []
    argv_iter = iter(argv)
    for arg in argv_iter:
        if arg == "-f":
            try:
                path = next(argv_iter)
            except StopIteration:
                print("error: argument -f: expected FILE", file=sys.stderr)
                sys.exit(1)

            if path in _pathlist:
                print(f"error: circular reference in -f files: '{path}' was already opened", file=sys.stderr)
                sys.exit(1)
            _pathlist.add(path)
            file_args = parse_argfile(path)
            file_args = expand_argfile(file_args, _pathlist)
            _pathlist.remove(path)
            new_argv.extend(file_args)
        else:
            new_argv.append(arg)
    return new_argv
