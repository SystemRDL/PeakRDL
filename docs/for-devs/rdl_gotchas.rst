.. _rdl_gotchas:

SystemRDL Gotchas
=================

SystemRDL is a relatively simple language, but writing a robust general-purpose
exporter can still be daunting. The intent of this guide is to provide a checklist
of some of the lesser-known, and commonly overlooked features of SystemRDL that
tool developers may want to be aware of.

It is important to emphasize: An exporter does *not* need to support all the features
of SystemRDL. Exporters should strive to support what is applicable, but also
should communicate to the user if a specific RDL construct is not supported.

When reading the checklist below, ask yourself the following questions:

* Does my PeakRDL extension support this scenario? Should it?
* If not, is it because the scenario is irrelevant to my application? Or is it a limitation in my tool?
* If it is a limitation, does my extension validate and warn the user that it is not supported?

To be clear, "limitations" are normal and often necessary. Some of the
edge-cases described below are borderline preposterous, but do show up in the
wild sometimes. It is good practice to anticipate them (even if the result is
to notify the user with an error).



SystemRDL allows deeply-nested designs
--------------------------------------
It is generally not safe to assume that a SystemRDL design will simply be a flat
list of ``reg`` components inside an ``addrmap``. SystemRDL allows
complex concepts to be expressed using nested ``regfile`` components, nested
subsystems using additional sub-``addrmap`` instances, and virtual memory
structures using ``mem`` components.

Consider the following simple example with slightly more complex hierarchy:

.. code-block:: systemrdl

    addrmap my_device {
        default sw = rw;
        default hw = r;

        reg {
            field {} mode[15:8] = 0;
            field {} enable[0:0] = 0;
        } control;

        regfile generic_buffer {
            reg {
                field {} addr[31:0];
            } start_address;

            reg {
                field {} n_bytes[31:0];
            } length;
        };

        generic_buffer rx_buffer_cfg;
        generic_buffer tx_buffer_cfg;
    };



SystemRDL identifiers may be repeated in different scopes
---------------------------------------------------------
As shown in the prior example, the RX and TX instances of ``generic_buffer`` results
in two copies of the ``start_addr`` and ``length`` registers. In SystemRDL this
is ok since they are under two distinct hierarchies so they are unambiguous.

If your exporter performs hierarchy flattening, this can pose a problem: Be
careful to not accidentally create a name collision. One easy strategy to avoid
this is to use the full hierarchy of an object (via ``Node.get_path()``) to
ensure names are distinct.

Another situation where this can arise is type name identifiers. Consider this example:

.. code-block:: systemrdl

    field {
        sw = r; hw = w;
        enum state_e {
            IDLE = 0;
            RECEIVING = 1;
            DISCONNECTED = 2;
        };
        encode = state_e;
    } rx_state[7:0];

    field {
        sw = r; hw = w;
        enum state_e {
            IDLE = 0;
            SENDING = 1;
        };
        encode = state_e;
    } tx_state[7:0];

Note how there are two distinctly different enumerations that are both named ``state_e``.
If your exporter is using the type name as-is in a common namespace, this could
pose a problem since the identifiers may collide. Again the hierarchical path
can be used to disambiguate, or the lexical scope path can be queried using
``get_scope_path()`` for most type definitions.



Instances may be N-dimensional arrays
-------------------------------------
Arrays are very useful when describing repeated structures in a design.
Most common are 1-dimensional arrays, but SystemRDL allows arrays to be of
arbitrary dimensions.

Any addressable component can be instantiated as an array: ``reg``, ``regfile``, ``mem``, ``addrmap``.

.. code-block:: systemrdl

    reg coefficient {
        field {} k[7:0] = 0;
    };

    // a 3x3 matrix of registers
    coefficient transformation_matrix[3][3] @ 0x0 += 0x4;



Arrays can be "sparse"
----------------------
SystemRDL does not require arrays of elements to be packed tightly.
Note how in the following example, each register element is 4-bytes, but the
stride between array elements is 16 bytes:

.. code-block:: systemrdl

    reg my_reg {
        regwidth = 32;
        // (contents not shown)
    };

    // a sparse array
    my_reg my_array[256] @ 0x0 += 0x10;



Registers and fields can sometimes overlap and occupy the same space
--------------------------------------------------------------------
Normally SystemRDL does not allow for registers or fields to occupy the same
positions. However, if the overlapping components do not have conflicting ``sw``
access policies, this is permitted.

.. code-block:: systemrdl

    field ro_field {sw = r; hw = w;};
    field wo_field {sw = w; hw = r;};

    // Registers are allowed to overlap since one is read-only and the other is write-only
    reg {
        ro_field f;
    } a @ 0x0;
    reg {
        wo_field f;
    } b @ 0x0;


    // Fields are allowed to overlap for the same reason
    reg {
        ro_field f1[7:0];
        wo_field f2[7:0];
    } c @ 0x300;



Beware of references to other components
----------------------------------------
Some SystemRDL properties can be assigned references to other components.
This is a useful mechanism to describe advanced behavior, but can also result
in some pretty complex structures.

Whenever querying ``Node.get_property()``, be sure to check which possible types
it can return. References can sneak up in unexpected places.

For example, a field's reset value is most often an integer, but it can also be a reference!

.. code-block:: systemrdl

    signal my_alt_reset_value[8];

    field {
        sw = rw;
    } my_field[8] = my_alt_reset_value;

In the above case, ``get_property("reset")`` will return a reference to a signal.

To help you catch all these cases, type-hint overloads are provided for all
variations of ``Node.get_property()``.



Register widths may not be what you expect
------------------------------------------
Do not always assume that a register is 32-bits wide. Be sure to query the
``regwidth`` property. Some devices can even have different register widths
within the same register file!

.. code-block:: systemrdl

    reg {
        regwidth = 32;
        // (contents not shown)
    } r32;

    reg {
        regwidth = 8;
        // (contents not shown)
    } r8;

    reg {
        regwidth = 256;
        // (contents not shown)
    } r256;



Beware of how registers may become unaligned
--------------------------------------------
SystemRDL has no requirement that registers be aligned to their register width.
It is rare that unaligned registers are actually used in designs. Often this
is typo by a user, but in some cases it can be intentional. Depending on the
output you are generating, this may or may not make sense to actually support.

Beware that unaligned registers can happen through multiple mechanisms:

.. code-block:: systemrdl

    addrmap top {
        reg my_reg {
            regwidth = 32;
            field {} f;
        };

        // Can be unaligned directly
        my_reg r1 @ 0x1; // <-- offset not a multiple of 4

        // Stride can cause misalignment
        my_reg r2[4] @ 0x10 += 0x6; // <-- stride not a multiple of 4

        // parent blocks could be misaligned
        regfile {
            my_reg r1 @ 0x0;
            my_reg r2 @ 0x4;
        } rf @ 0x102; // <-- offset not aligned
    };

See the resulting absolute addresses as shown by PeakRDL's ``dump`` command:

.. code-block::

    $ peakrdl dump example.rdl --unroll
    0x001-0x004: top.r1
    0x010-0x013: top.r2[0]
    0x016-0x019: top.r2[1]
    0x01c-0x01f: top.r2[2]
    0x022-0x025: top.r2[3]
    0x102-0x105: top.rf.r1
    0x106-0x109: top.rf.r2



References to out-of-scope signals
----------------------------------
It is legal SystemRDL to reference signals that are instantiated in a parent
namespace. This includes the root namespace.

Depending on how you implement your exporter, these may pose a special case since
such a signal would not be encountered if iterating descendants of the top-level
addrmap.

.. code-block:: systemrdl

    signal my_signal[8];

    addrmap top {
        reg {
            field {
                sw = rw;
            } my_field[8] = my_signal;
        } r1;
    };



External Components
-------------------
In SystemRDL, components such as ``regfile`` and ``reg`` can optionally be
declared as ``external``. The ``addrmap`` and ``mem`` components are always
considered external.

The interpretation of what an "external" component means may influence how your
exporter operates.
For example in PeakRDL-regblock, external components will not be implemented
within the register file, and instead infer an external access port for the user
to connect.
In other cases like the PeakRDL-html documentation generator, whether something
is internal or external is irrelevant.

If the concept of internal/external component is theoretically relevant in your
exporter but not supported, it is good practice to validate the user's input and
warn if it is encountered.



Beware of msb0 mode
-------------------
A seldom-used, but possible mode described in SystemRDL (section 10.7) is msb0
mode.

In some cases, this may imply a bitswap operation on register fields. The
``RegNode.is_msb0_order`` property provides and easy way to detect ths condition.
