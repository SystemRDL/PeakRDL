Argument Files
==============

PeakRDL supports reading argument files using the ``-f FILE`` flag.
Argument files can be used to provide source file lists, or to simply reduce the
amount of text provided in the command-line.

Argument files contain additional command-line text, as well as a few other
things described below.


Comments
--------
Anything after a ``#`` character is treated as a comment and is discarded.


Nested -f Flags
---------------
Argument files can include other additional argument files by using the ``-f``
flag.


Environment Variables
---------------------
Argument files can contain references to environment variables. Both
``$VAR_NAME`` and ``${VAR_NAME}`` styles are supported.


Anchor to current directory
---------------------------
If referencing files that are relative to an argument file, the
``${{this_dir}}`` token can be used. This token expands to the directory path
that contains the current agument file.
