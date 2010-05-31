Overview
========

bit is an easy to use, easy to modify, and easy to understand build system.  
It has an easy to use API, and is great for those small projects.   

Information
-----------

Currently only python 2.6.x is supported, though there are plans to add in Python 3.x support.  
No python versions before that will be supported.  
buildit is not guaranteed to run on other Python implementations.  

Installation Instructions
-------------------------

To install bit, merely run `python setup.py install` in your favorite shell

Building The Documentation
--------------------------

The documentation is written using markdown syntax, and can be viewed in an HTML format via github.

Tutorial
========

Here is a small and quick tutorial to showcase the ease of use that bit gives to you, the developer. Just place some code like so in a file named "bitfile"

    x = Project('ArbitraryProjectName')
    x.files('source') # Grabs all files in source
    x.rmdir('source/arbitrary_platform') # buildit will ignore all files in this directory.
    bit.project(x)


Roadmap
=======

Version 0.3 - Caress of Steel
-----------------------------

 * C/C++/ObjC Support
 * Shiny New API 
 * Markdown Based Documentation (Read it directly here on github!)
 * Actual File to run via a script called "snake"

Contributors
------------

Tres Walsh (SAHChandler)

This project is released under a BSD License (Please see License.md)
