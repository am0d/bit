Cocoa
=====

Cocoa is the OS X specific project type for C, C++, and Objective-C projects. This documentation shows functions that are specific to Cocoa. For the rest of the list, see `Unix`.  

Functions
---------

### framework ###

Takes any number of strings that are then added to the build command in the form of `-framework <framework_name>`. 

### arch ###

Takes any number of strings that are added to the commandline for building universal binaries. As long as a specific version of GCC or clang supports a specific architecture, the given platform will work fine.

