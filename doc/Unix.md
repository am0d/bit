Unix
====

`Unix` is the go to project for basic C, C++, and Objective-C based projects. Both `Cocoa`, and `MinGW` inherit all of the following functions and properties from `Unix`. In addition, `Unix` inherits from `Project`, which should never be used in any bit projects. The default compiler for `Unix` is `CC`, but can be changed to any other compiler from the `bit.compiler` module. 

Functions
---------

### pkg ###

Takes any number of strings, and then adds the `<string>-config --cflags --libs` to the proper build commands.

### pkg_config ###

Takes any number of strings and then adds the output of `pkg-confg <string> --cflags --libs` to the proper build commands.

### define ###

All arguments are passed on to the compiler's `define` function.

### incdir ###

All arguments are passed on to the compiler's `incidr` function.

### libdir ###

All arguments are passed on to the compiler's `libdir` function.

### library ###

All arguments are passed on to the compiler's `library` function.

### cflags ###

All arguments are passed on to the compiler's `cflags` function.

### lflags ###

All arguments are passed on to the compiler's `lflags` function.

### flags ###

All arguments are passed on to both the compiler's `lflags`, and `cflags` function.

Properties
----------

### C99 ###

Enables the C99 property of the compiler.

### CXX ###

Enables C++ and Objective-C++ support in the compiler, while disabling C support

### CPP ###

Does the same thing as `Unix.CXX`

### enable_c ###

Re-enables C support for a C++ project.

### clang ### 

Sets `Unix`'s compiler to the clang compiler.
