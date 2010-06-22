bit tutorial
============

The following tutorial will walk a beginner through setting up bit, as well as it's internal workings.

* Overview
* Installing bit
* The bitfile

Overview
--------

In this small tutorial, we're going to get you (the user) up and running with bit.

Installing bit
--------------

bit (0.3) currently requires a python 2.6 installation. It is known to work on Mac OS X, Linux, and Windows. To install bit, merely use the classic `setup.py install` from the commandline. On Windows, you will need to make sure that the <python installation path>\Scripts is on your system `PATH`. This is so that the `bit` commandline app can be used. On OS X and Linux, these are automatically added to a folder on your PATH (assuming you're not doing anything wonky)

The bitfile
-----------

To use bit, you will need to create a bitfile in your given directory. Naming it "bitfile" will suffice for the purposes of this tutorial, however like `make`, bit supports the use of whatever named file you would like via `bit -f <file_name>` on the command line.  

A bit file is nothing more than a python script, with (most) of the necessary imports taken care of for you.

Let's look at a very basic bitfile for an OpenGL project using [SDL][1]

    if windows:
        Project = MinGW
    if macosx:
        Project = Cocoa
    if linux:
        Project = Unix

    opengl = Project('bit_tutorial')
    opengl.files('src')
    opengl.incdir('include')

    if macosx:
        opengl.framework('OpenGL')
        opengl.arch('i386', 'x86_64')
    if windows:
        opengl.library('opengl32')
    if linux:
        opengl.library('GL')

    opengl.pkg('sdl')
    bit.project(opengl)

So let's walk through the above text.

[1]: http://libsdl.org "SDL Library"
