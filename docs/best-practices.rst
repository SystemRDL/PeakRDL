SystemRDL Best Practices
========================

Avoid global scope
------------------
Only use the global lexical scope if you want to declare common components that
you intend to use globally. This avoids polluting the global namespace and
prevents unexpected component name collisions.

|:thumbsdown:| Bad:

.. code:: systemrdl

    reg my_ctrl_reg {
        ...
    };

    reg my_status_reg {
        ...
    };

    addrmap my_device {
        my_ctrl_reg ctrl;
        my_status_reg status;
    };

|:thumbsup:| Good:

.. code:: systemrdl

    addrmap my_device {
        reg my_ctrl_reg {
            ...
        };

        reg my_status_reg {
            ...
        };

        my_ctrl_reg ctrl;
        my_status_reg status;
    };


When to use addrmap vs regfile
------------------------------
The ``addrmap`` and ``regfile`` components are very similar. Sometimes it is not
clear which you should use.

regfile
    Use a regfile when describing a *conceptual* grouping of registers inside
    a peripheral's register block.
    Regfiles are useful to group similar concepts together to make your register
    space logically organized.
    A regfile does not imply any physical boundary in the hardware implementation.

addrmap
    An addrmap is used to describe a grouping that *physically* separates
    subsystems in a design. An addrmap may be used to represent the top-level node
    of a peripheral's register block, a grouping of peripherals, or the top-level
    of your SoC.


Use default assignments
-----------------------
Default assignments are an easy way to override the default value of an assignment
within a lexical scope. These are very useful for common properties like ``sw``
and ``hw`` in control or status registers that have many fields with similar behavior.

Without default assignments:

.. code:: systemrdl

    reg my_control_reg {
        field {
            sw = rw;
            hw = r;
        } a;

        field {
            sw = rw;
            hw = r;
        } b;

        field {
            sw = rw;
            hw = r;
        } c;
    };

With default assignments:

.. code:: systemrdl

    reg my_control_reg {
        default sw = rw;
        default hw = r;

        field {} a;
        field {} b;
        field {} c;
    };

.. tip::

    Use default assignments in the most local lexical scope that is appropriate.
    This improves readability, and prevents the assignment from affecting
    something you didn't intend.

    Avoid using default assignments in the root namespace.
