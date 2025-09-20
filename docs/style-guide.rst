SystemRDL Style Guide
=====================
Style guides can be a helpful way to ensure code readability and build common
best-practices. These are not hard rules, but rather they are recommendations
to follow so that your SystemRDL is readable and beautiful to everyone that
comes across it. Since all style guides are inherently opinionated, it is
important not to take them too seriously. It is ok to break from the style
guide if it will improve readability and consistency.



Indentation is 4 spaces per level
---------------------------------

Do not use tabs. Use spaces for indentation.
Configure your text editor to emit spaces when you press the tab key.

When to indent
--------------
Always add a level of indentation for component contents, enum contents,
parameter lists, or anything else between braces: ``{``, ``}``, ``(``, ``)``,

Keep indentation consistent
---------------------------

|:thumbsup:| Yes:

.. code:: systemrdl

    field {
        desc = "My field";
        sw = rw;
        hw = r;
    } my_field;

|:thumbsdown:| No:

.. code:: systemrdl

    field {
        desc = "My field";
          sw = rw;
    hw = r;
    } my_field;


Braces and Parentheses
----------------------
The opening brace ``{`` must be on the same line as the statement it belongs to.
The closing brace ``}`` must be on a line of its own along with its instance
name if appropriate.


|:thumbsup:| Yes:

.. code:: systemrdl

    field {
        desc = "My field";
        sw = rw;
        hw = r;
    } my_field;

|:thumbsdown:| No:

.. code:: systemrdl

    field
    {
        desc = "My field";
        sw = rw;
        hw = r;
    }
    my_field;

If a component has a parameter list, parentheses use the same convention:

|:thumbsup:|

.. code:: systemrdl

    field my_field #(
        longint unsigned MY_PARAM = 1,
        longint unsigned OTHER_PARAM = 2
    ){
        desc = "My field";
        sw = rw;
        hw = r;
    };

    my_field #(
        .MY_PARAM(2),
        .OTHER_PARAM(3),
    ) inst;


Where to add spaces
-------------------

On both sides of any assignment or expression operators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|:thumbsup:| Yes:

.. code:: systemrdl

    reset = 4 + MY_PARAM / 2;

|:thumbsdown:| No:

.. code:: systemrdl

    reset=4+MY_PARAM/2;

Before and after open/close braces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|:thumbsup:| Yes:

.. code:: systemrdl

    field {
        desc = "My field";
    } my_field;

|:thumbsdown:| No:

.. code:: systemrdl

    field{
        desc = "My field";
    }my_field;

Exception is if the next item after a closing brace is a semicolon: ``};``


Only one property assignment per-line
-------------------------------------

In most cases, keep each property assignment on its own distinct line.
Since properties ``sw`` and ``hw``, are nearly always used together, it is
acceptable to stack them on the same line.

|:thumbsup:| Yes:

.. code:: systemrdl

    field {
        desc = "My field";
        sw = r;
        hw = na;
        counter;
        onread = rclr;
    } my_field;

|:thumbsdown:| No:

.. code:: systemrdl

    field {
        desc = "My field";
        sw = r; hw = na; counter; onread = rclr;
    } my_field;


|:thumbsup:| Acceptable:

.. code:: systemrdl

    field {
        desc = "My field";
        sw = r; hw = na;
        counter;
        onread = rclr;
    } my_field;


Component type and instance names are lowercase
-----------------------------------------------
There is no need to yell.

|:thumbsup:| Yes:

.. code:: systemrdl

    field my_field {
        ...
    };

    my_field inst;

|:thumbsdown:| No:

.. code:: systemrdl

    field MY_FIELD {
        ...
    };

    MY_FIELD INST;

.. note::
    If you are transcribing a datasheet or other source material into SystemRDL,
    and that uses upper-case for register/field names, use the original case unchanged.


Parameters and Verilog-style macros are uppercase
-------------------------------------------------
Constants should be in ALL_CAPS

|:thumbsup:|

.. code:: systemrdl

    field my_field #(
        longint unsigned MY_PARAM = 1,
        longint unsigned OTHER_PARAM = 2
    ){
        // ...
    };


|:thumbsdown:|

.. code:: systemrdl

    field my_field #(
        longint unsigned my_param = 1,
        longint unsigned other_param = 2
    ){
        // ...
    };


Long descriptions
-----------------

Break long descriptions into multiple lines, indented at the same level as the
scope it is in.
Start and end quotation marks use the same rules as braces.

|:thumbsup:|

.. code:: systemrdl

    field {
        desc = "My short description";
    } my_field_a;

    field {
        desc = "
        This is a long description.

        It requires multiple lines that are all indented at the same level.
        ";
    } my_field_b;


Avoid unnecessary prefixes in names
-----------------------------------

SystemRDL is a hierarchical language. There is no need to prefix registers with
the device name, or fields with the register name. Each hierarchy is a distinct
instance scope, so no need to worry about name collisions.

|:thumbsdown:| No:

.. code:: systemrdl

    addrmap spi_controller {
        reg {
            default sw = rw;
            default hw = r;

            field {} spi_ctrl_enable;
            field {} spi_ctrl_reset;
            field {} spi_ctrl_mode;
        } spi_ctrl;
    };


|:thumbsup:| Yes:

.. code:: systemrdl

    addrmap spi_controller {
        reg {
            default sw = rw;
            default hw = r;

            field {} enable;
            field {} reset;
            field {} mode;
        } ctrl;
    };
