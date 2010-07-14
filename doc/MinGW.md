MinGW
=====

MinGW is a Windows specific project type for GCC projects. This documentation shows the functions that are specific to MinGW. For the rest of the list see `Unix`

Functions
---------

### resource ###

Takes any number of windows resource (.rc) files. These are then compiled to object files with `windres`, and placed in the proper directory, and then linked in the with project. Use this to embed icons and other resources into your executable.  

Properties
----------

### resource_compiler ###

Takes a string that is then searched for on the syytem `PATH`. Use this to allow for different resource compilers on windows, or, if using a cross compiler, such as `i586-mingw32-windres` on Linux.
