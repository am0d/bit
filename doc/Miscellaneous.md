Miscellaneous
=============

This documentation file list several extra variables and instances of objects that the user should be aware of. It also details the different commandline options that are available with bit.

Global Booleans
---------------

There are several global booleans that are "reserved" by bit. These are:  

 * macosx
 * windows
 * linux
 * bsd

Each of these are set to `True` on their respective platforms.

Global Instance
---------------

There is a global instance of a type called `GPL`, which stands for global project lookup. This is where all the projects are stored. It can be accessed as the variable `bit`.

Notes
-----

It is important that users of bit understand that a bitfile is in fact a python script. While bit takes care of importing itself, if use of the python stdlib is desired it must be imported as if it were a normal python script.

