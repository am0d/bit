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

bit (0.3) currently requires a python 2.6 installation. It is known to work on Mac OS X, Linux, and Windows. To install bit, merely use the classic `setup.py install` from the commandline. On Windows, you will need to make sure that the [python installation path]\Scripts is on your system `PATH`. This is so that the `bit` commandline app can be used. On OS X and Linux, these are automatically added to a folder on your `PATH` (assuming you're not doing anything wonky)

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
        opengl.framework('Cocoa', 'OpenGL')
        opengl.arch('i386', 'x86_64')
    if windows:
        opengl.library('opengl32')
    if linux:
        opengl.library('GL')

    opengl.pkg('sdl')
    bit.project(opengl)

So let's walk through the above text.  

The `if <platform>` block shows the variables `windows`, `macosx`, and `linux`. These are of a boolean type and are defined by bit. They return true on their respective platforms. The `Project` variable is then set to one of `MinGW` (a `gcc` based project on Windows), `Cocoa` (also `gcc`) and `Unix`, which is a generic `cc` and `c++` project.  

Next we create our instance of `Project`. All `Project` classes in bit take an argument that will be the name of the output file, in this case, we'll have an executable output as `bit_tutorial`. With `opengl.files('src')` we add tell bit to look for files in the directory `src` which is relative to the bitfile's position. After that a call to `opengl.incdir('include')` informs bit to add the include path to whichever compiler's include option (`-I ./include/` for gcc)  

In our next `if <platform>` block, we go about adding platform specific libraries (and in OS X's case, architectures) to the project. Of note is that Mac OS X supports both the traditional `.library('foo', 'bar', 'baz')` and the OS X specific `.framework('foo', 'bar')` functions. One thing to note here is that all bit project functions take variable arguments, so for instance, `opengl.files('src1', 'src2', 'src3') will work by adding all 3 directories to bit.  

Finally we have two interesting functions. `opengl.pkg('sdl')` is equivalent to placing `sdl-config --cflags --libs` in a makefile. This is intended to work for all `<script>-config` such as '`wx-config`, amongst other projects. If you want to use `pkg-config`, you can simply use `.pkg_config('foo', 'bar', 'baz')`. Lastly, we need to register the opengl project with bit. This is to allow us to either use threaded projects (running many at once), or run the projects sequentially.  

Hopefully this tutorial has shown you how simple it is to use bit. Check out the rest of the documentation to learn more about bit. 

[1]: http://libsdl.org "SDL Library"
