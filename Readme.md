Overview
========

buildit is an easy to use, easy to modify, and easy to understand build system.  
It supports dependency tracking, multiple projects, and an easy to use API.  

Information
-----------

Currently only python 2.6.x is supported, though there are plans to add in Python 3.x support.  
No python versions before that will be supported.  
buildit is not guaranteed to run on other Python implementations.  

Installation Instructions
-------------------------

To install buildit, merely run `python setup.py install` in your favorite shell

Building The Documentation
--------------------------

Chances are that the documentation will be placed here on github, either via the project wiki, or in a doc folder in markdown format. 

Tutorial
========

Here is a small and quick tutorial to showcase the ease of use that buildit gives to you, the developer. Just place some code like so in a file named "snakefile"

    x = Project('ArbitraryProjectName')
    x.add_files('source') # Grabs all files in source
    x.remove_directory('source/arbitrary_platform') # buildit will ignore all files in this directory.
    buildit.add(x)


Roadmap
=======

Version 0.3 - Caress of Steel
-----------------------------

 * C/C++/ObjC/ooc Support
 * Shiny New API 
 * Proper Dependency Tracking
 * Python Style Documentation (Sphinx)
 * Possible Plugin Architecture
 * Actual File to run via a script called "snake"

Contributors
------------

Tres Walsh (SAHChandler)

This project is released under a BSD License (Please see License.md)
