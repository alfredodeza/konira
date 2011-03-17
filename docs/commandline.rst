.. _commandline:

The Command-line
================
*Konira* ships with some basic (yet useful) command line options. You 
can control the type of output and how the tool behaves when there 
is a failure.

In this section we will cover all of the command-line options and give
examples on how each of them affects your tests.


help
----
The tool's help menu is often the fastest way to access some information
about command-line options, it can be triggered with any of these command
switches:

 * ``-h``
 * ``help``
 * ``--help``
 * ``help``

The over redundant help flags make it up for the lack of a standard in
triggering help menus in command line tools. You just can't miss it.


Running tests
=============
Running your tests is as easy as calling the *Konira* executable at the 
command line. However, there are a few features that you might want to 
be aware of so you can control the output and behavior of tests.


Auto Discovery
--------------
Auto discovery is the default behavior of *konira*. However, you need to follow
the naming convention that makes your tests discoverable. All the tests that
you want to get executed must have their filename start with ``case_``.

The following filenames would match correctly for autodiscovery:

 * ``case_foo.py``
 * ``Case_foo.py``
 * ``CASE_foo.py``


Specific Paths
--------------
In some occasions you may want to better specify a path for test collection.
This is useful when you don't want to run every single test on your path but
a certain portion.

You do not need to provide a path for test collection and execution because
*konira* has auto discovery by default, but in the case you need to, you would
do it like this::

    konira /path/to/tests


.. _specific-classes:

Specific Classes
----------------
If you want to match classes (that *konira* sees as "describe") you have two
options, you can add them to an absolute path or you can use the ``describe``
switch.

The path option would look like this::

    konira "/path/to/tests::my class"

Note how the path is now quoted. This is necessary for most shells as the path
may have whitespace and this allows for some misinterpretation of the actual
value. This value needs to be the same as the string you are using to describe
your test scenario.


The command line switch option would look like this::

    konira describe "my class"


This, also needs quotes around it, so that the shell interprets it correctly.
Any scenarios that match that describe exactly will be executed.


.. _specific-methods:

Specific Methods
----------------
When you need specific methods (as with :ref:`classes`) you can solve this
approach in two different ways: with an absolute path or with the ``it``
command line switch.

The path option would look like this::

    konira "/path/to/tests::my class::my method"

Again, note that the path is quoted to avoid shell issues.

The command line switch would look like this::

    konira it "should evaluate to true"

The ``it`` switch also needs the parameter to be quoted, and it will search
every child path and collect every tests that matches that string.
    

stdout and stderr capturing
===========================
Because most of the time you do not need huge output, or extremely verbose 
output, *konira* offers some options to control it when you run your tests.



Stop at first fail
==================

Output
======

Tracebacks
----------

Dotted
------


