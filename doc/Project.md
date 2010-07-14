Project
=======

`Project` is the primary root object from which all other project typs inherit. All the functions available in `Project` are available in all other project types.  

Functions
---------

### append_step ###

Takes a function that is added onto the end of the build_steps.

### prepend_step ###

Takes a function that is placed at the front of the build steps.

### insert_step ###

Takes a function and a location, whherein the function is inserted into the location of the build steps. (i.e. `insert_step(arbitrary_function, 3)` will insert `arbitrary_function` at `build_steps[3]`

### is_complete ###

A boolean that signifies whether or not the project has successfully completed it's build steps.

### directory ###

Takes any number of strings which are then treated added to the list of files to build. This function only takes directories, and will not search child directories.

### files ###

Takes any number of strings and adds it to the list of files to build. This function autoglobs, and traverses subdirectories, as well as takes single named files.

### rmdir ###

Takes any number of strings which are then matched against files in the current list of files to compile. Only place directories, and not single files.

### rmfiles ###

Takes any number of strings which are then removed from the currently built list of files to compile. This function autoglobs, and traverses subdirectories to perform the operation. It can take either directories, or files. 

### require ###

This takes exactly one instance of another project. This will ensure that the required system is compiled before the project that calls this function. 

Properties
----------

### name ###

This returns the name of the project type in a string. 

### static ###

This instructs the project to attempt to output a static library.  

### binary ###

This is the default setting. The project's compiler will attempt to output an executable binary.

### dynamic ###

This instructs the project to attempt to output a dynamic library. 
