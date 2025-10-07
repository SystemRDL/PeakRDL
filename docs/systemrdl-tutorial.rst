SystemRDL Tutorial
==================

SystemRDL is the primary input language recommended for the PeakRDL toolchain.
This tutorial is intended to be a quick introduction of some basic SystemRDL
concepts. For more in-depth details, see the official
`SystemRDL specification <http://accellera.org/downloads/standards/systemrdl>`_.



Component Types
---------------
There are several component types that make up the building-blocks of any
SystemRDL address map description.

field
    A ``field`` is the lowest-level component in SystemRDL. It describes the
    behavior of a collection of bits within a register.
    A field is also the most configurable component in the SystemRDL language.
    It has the most number of properties dedicated to it and can be configured
    into countless behaviors.

reg
    A register is a container for one or more fields that are accessible by
    software at a given address.

regfile
    A register file is a logical grouping of registers or additional register
    files. The ``regfile`` is a convenient mechanism to group
    conceptually-related registers together within a design.

addrmap
    An address map is also a grouping of all of the above, but it also implies
    a physical boundary in an implementation. SystemRDL does not attempt to
    imply what this boundary is, but it is usually the boundary of a register
    block module in RTL, an encapsulation of an IP or subsystem, etc.

signal
    Signals provide a mechanism to define additional inputs into the register
    map so that they can augment the behavior of components.
    Usually signal references are assigned to various component properties.

mem
    A memory represents an array of storage elements in your design.
    You can optionally instantiate registers inside a memory to imply structure.



Defining and instantiating components
-------------------------------------

Basics
^^^^^^
There are two ways to define a component:

Named Definition
    Named definitions are useful if you plan to re-use the component multiple
    times. The named definition can be instantiated multiple times.
    For example, a ``field`` definition + instantiation may look like this:

    .. code-block:: systemrdl

        // Define the component once
        field my_field_type {
            // (component body)
        };

        // Instantiate it multiple times
        my_field_type field_instance_1;
        my_field_type field_instance_2;
        my_field_type field_instance_3;

Anonymous Definition
    An anonymous definition is a shorthand way of defining a component without a
    type name. Anonymous definitions are immediately instantiated.
    These are useful if you do not intend to re-use the field definition
    multiple times.

    .. code-block:: systemrdl

        field {
            // (component body)
        } field_instance;


Arrays
^^^^^^
The ``reg``, ``regfile``, ``addrmap``, and ``mem`` components can be
instantiated as an array of instances. Arrays can have multiple dimensions.

.. code-block:: systemrdl

    reg my_reg_type {
        // (component body not shown)
    };

    my_reg_type reg_array[16]; // 16-element array. 0 to 15
    my_reg_type reg_array_3d[4][4][4]; // 3-dimensional array. 64 total elements



Specifying the position of an instance
--------------------------------------

Fields
^^^^^^
If left unspecified, the bit-position of a field is allocated sequentially.
Otherwise, you can explicitly define the field position:

.. code-block:: systemrdl

    my_field_type field_1[3:0]; // 4-bit wide field at bit position [3:0]
    my_field_type field_2[4]; // another 4-bit wide field, implied at position [7:4]
    my_field_type field_3; // single-bit field at a bit-offset of 8
    my_field_type field_4[16:16]; // single-bit field at bit offset 16

Often, it is necessary to specify a field's reset value. This is done using the
reset assignment operator:

.. code-block:: systemrdl

    my_field_type field_1[7:0] = 42; // field has a reset value of 42


Addressable Components
^^^^^^^^^^^^^^^^^^^^^^
``reg``, ``regfile``, ``addrmap`` and ``mem`` components all get allocated to
an address in the register map.
If un-specified, the address is automatically assigned sequentially.
It is best practice to allocate addresses explicitly. All address offsets are
relative to the parent component. SystemRDL always uses byte addressing.

.. code-block:: systemrdl

    my_reg_type reg_1 @ 0x1000; // is at address offset 0x1000

To define the spacing between elements in an array, use the array stride
allocation operator: ``+=``

.. code-block:: systemrdl

    // reg_array[0] @ 0x1000
    // reg_array[1] @ 0x1010
    // reg_array[2] @ 0x1020
    // etc ...
    my_reg_type reg_array[16] @ 0x1000 += 0x10;



Assigning properties
--------------------
SystemRDL properties are used to annotate the details of a component and its
behavior. For a full listing of properties, see the
`SystemRDL specification <http://accellera.org/downloads/standards/systemrdl>`_.

Properties can be assigned directly:

.. code-block:: systemrdl

    field {
        name = "My awesome field";
        desc = "A longer description of what this field does";
        sw = rw;
        hw = r;
    };

If a boolean property has no value assigned, it is implied to be true:

.. code-block:: systemrdl

    counter;
    // implies: counter = true;

Properties of an instance can be overridden:

.. code-block:: systemrdl
    :emphasize-lines: 7

    field my_awesome_field {
        name = "My awesome field";
    };

    my_awesome_field field_1;

    field_1->name = "My overridden name";


You can specify a 'default' property assignment.
This will automatically be applied to all component definitions enclosed in the
lexical scope:

.. code-block:: systemrdl
    :emphasize-lines: 1, 4

    default sw = rw;

    field my_awesome_field {
        // implied: sw = rw;
    };


Some properties accept references to other components:

.. code-block:: systemrdl
    :emphasize-lines: 4

    my_awesome_field field_1;
    my_awesome_field field_2;

    field_1->reset = field_2; // field_1 will get field_2's value when reset.


Or references to other properties:

.. code-block:: systemrdl
    :emphasize-lines: 7-8

    field {
        counter;
    } my_counter[7:0];

    my_awesome_field field_1;

    // my_counter will increment every time field_1 is accessed by software
    my_counter->incr = field_1->swacc;


Parameterized Components
------------------------
Just like in HDL languages, SystemRDL lets you parameterize components.
This allows you to define generic components that can be re-used with different
parameterizations.

.. code-block:: systemrdl

    reg my_reg_type #(longint SIZE = 4, bit RESET = 4'hF) {
        field {} f1[SIZE - 1: 0] = RESET;
    };

    my_reg_type r1; // Default parameterization
    my_reg_type #(.SIZE(8)) r2;
    my_reg_type #(.SIZE(16), .RESET(16'hABCD)) r3;


Enumerated Fields
-----------------
In most cases, a field will represent a numeric value in your design. However,
sometimes it is useful to ascribe names to enumerated values using an RDL ``enum``.
An enumeration can be bound to a field using the ``encode`` property.

.. code-block:: systemrdl

    // An enum associatyes names with values
    enum system_state_e {
        IDLE = 0 {
            desc = "The system is idle and ready for input";
        };

        BUSY = 1 {
            desc = "Busy processing an input";
        };

        SLEEP = 2; // No properties assigned
        SHUTDOWN; // Infers value of 3
    };

    field {
        encode = system_state_e;
        reset = system_state_e::IDLE;
    } system_state[1:0];


Some Examples
-------------
Here are a few interesting examples of what you can do with SystemRDL.
There are countless of combinations possible, so just go ahead and look through
the `SystemRDL specification <http://accellera.org/downloads/standards/systemrdl>`_
to learn more!

.. code-block:: systemrdl

    field rw_field {
        // A field that is read and writable by software
        sw = rw;
        // and whose value is visible to hardware
        hw = r;
    };

    // A read-only field driven by a hardware signal
    // No storage element
    field ro_field {
        sw = r;
        hw = w;
    };

    // a field that read/writable by software, but is also writable by hardware
    field hw_rw_field {
        sw = rw;
        hw = rw;
        we; // hardware has write-enable control.
    };

    // An up-counting counter
    field counter_field {
        sw = r;
        counter; // is a counter that infers an increment control hardware input signal
    };

    // Field that is set by hardware, and cleard by software read
    field event_flag_field {
        sw = r;
        hw = w;
        hwset; // Hardware control to set the field
        onread = rclr; // cleared when read by software
        precedence = hw; // if read and set at the same time, hardware wins.
    };
