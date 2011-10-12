.. _commandline:

The Command-line
================
*Konira* ships with some basic (yet useful) command line options. You 
can control the type of output and how the tool behaves when there 
is a failure.

In this section we will cover all of the command-line options and give
examples on how each of them affects your tests.


help
====
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

**But there is an exception!**

If somehow the default auto-discovery behavior does not suite your needs, there
is a flag that allows you to tweak the collection of cases ::

    konira --collect-match "matching-regex-here"

That can also be used with the case insensitive flag::

    konira --collect-match "matching-regex-here" --collect-ci

If you pass in a matching regular expression, it will directly affect the
collection of test cases.

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
When you need specific methods (as with :ref:`specific-classes`) you can solve this
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
Because most of the time you do not want stdout or stderr clovering the terminal, 
or extremely verbose output, *konira* offers some options to control it 
when you run your tests.

In certain occasions, the executing tests outputs to stdout and stderr. To
avoid this, the test runner captures both and does not allow anything other
than the runner's output.

There are to options that will force *konira* to avoid capturing stdout and
stderr: ``-s`` or ``no-capture``


Debugging with PDB
------------------
A separate note about PDB: since *konira* captures terminal output, ``pdb``
will not work when you want to step through your code or tests. It is almost
certain that a ``KoniraIOError`` will be raised and the affected test will be
registered as a failed test.

To avoid such an issue, if you need to use ``pdb`` you need to use either
``-s`` or ``no-capture``.


Debugging Konira
----------------
Konira makes an effort to remove unnecessary traceback information when
a failure or an error occurs. But sometimes (hopefully not often!) there might
be information that you need as part of the context of the exception. 

If you need to, there is a flag that will force the engine not to
overwrite/cleanup tracebacks and present them as they were raised::

    konira --debug

Stop at first fail
------------------
Probably one of the most common options amongst test runners: the stop at the
first failed test option. This is useful if you do not want the test runner to
keep moving forward executing other tests if a single one fails.

There are two options to achieve this: ``-x`` or ``fail``.


Output
======
The test runner is *very* minimalistic about output. You will not get full
tracebacks. 

Below you can see how a common ``AssertionError`` would be displayed

.. highlight:: koniraterm

::

    Failures:
    ---------

    1 ==> AssertionError
    Starts: /Users/alfredo/python/konira/tests/case_exc.py:363:
    Ends: /Users/alfredo/python/konira/exc.py:25:


The first line in the error tells you about the exception and appends any extra
information that the exception may have (none in this case).

The **Starts** section is where the exception started with an included line
number and the **Ends** is where it actually ends.

This information is great to know when the exception went through different
files and ended in a different file other than your actual test.

In case an exception started and ended in your test file, the failure
information would look like this::


    Failures:
    ---------

    1 ==> AssertionError
    Starts and Ends: /Users/alfredo/python/konira/tests/case_exc.py:363:


Tracebacks
----------

What if you want a traceback? The test runner allows you to have such a thing
with the ``-t`` or ``traceback`` switches::

    $ konira -t

    my class
        my test


    Failures:
    ---------

    1 ==> AssertionError
    Starts and Ends: /Users/alfredo/python/konira/tests/case_exc.py:362:
    Traceback (most recent call last):
      File "/Users/alfredo/python/vkonira/tests/case_exc.py", line 362, in it_my_test
        assert False
    AssertionError
    
    1 spec failed, 1 total in 0.000 secs.


Dotted
------
Finally, we have dotted support. If you have just a few tests, then this might
not make sense, but if you have more than a few dozen ones, it might not be
useful to have them all over your screen.

So dotted support will print dots ('.') for passing tests and 'F' for failed
ones.

The command line switches for dotted support are ``-d`` or ``dots``.


Coverage
========
As from version `0.0.5` konira includes support for Ned Batchelder's excellent 
coverage plugin.

.. note::
    Before using coverage make sure you have installed and available in your
    sys.path. Otherwise you will get an error message


The coverage has a couple of flags to control how output is determined, and for
now this is the flag that enables coverage output:

::

    konira cover

The output when coverage is used should look similar to this::

    ..........................................



    All 42 specs passed in 0.561 secs.
    Name                    Stmts   Miss  Cover
    -------------------------------------------
    foo/__init__                2      0   100%
    foo/cache                  53      4    92%
    foo/config                 23      0   100%
    foo/exc                     3      0   100%
    foo/log                    15      0   100%
    foo/middleware             66      6    91%
    -------------------------------------------
    TOTAL                     162     10    94%


With no other options passed in, `cover` will run a report on all the tests
executed.

You will notice that no missing lines will be printed. This is the default
behavior. 

To activate missing lines and display them, you need to enable the
`--show-missing` flag:

::

    konira cover --show-missing

Output when `--show-missing` is enabled should be similar to this::


    ..........................................



    All 42 specs passed in 0.561 secs.
    Name                    Stmts   Miss  Cover  Missing
    ----------------------------------------------------
    foo/__init__                2      0   100%
    foo/cache                  53      4    92%  62, 66-68
    foo/config                 23      0   100%
    foo/exc                     3      0   100%
    foo/log                    15      0   100%
    foo/middleware             66      6    91%  30, 51-55
    ----------------------------------------------------
    TOTAL                     162     10    94%


If you need to specify a single package or module you can pass such an option
to the `cover` flag. For example, if you were testing the module `foo` and
wanted specific output for `foo.bar` it would look like this:

::

    konira cover foo.bar


Profiling
=========
When the profiling command line flag is set, the normal red/green output is supressed 
for dotted output.

This is basically the best option to concentrate in the profiling data that gets rendered
at the end of the test run.

The `profile` option will show the 10 slowest tests in descending order and it should look
very similar to this::


    .....................................................

    Profiling enabled
    10 slowest tests shown:

    0.00034499 - It returns a valid diff when comparing strings
    0.00027298 - It returns valid dictionary comparisons
    0.00018191 - It does not translate a regular class
    0.00013995 - It raises a first fail exception
    0.00013399 - It does not translate a regular method
    0.00012707 - It translates a describe with inheritance
    0.00012016 - It translates a describe with inheritance regardless of space
    0.00011515 - It translates after each constructors
    0.00011396 - It parses and evaluates left values and text values with a not equal operand
    0.00011396 - It translates a describe with inheritance with a lot of whitespace


    All 185 specs passed in 0.148 secs.

The options to enable profiling are: `profile` or `-p`. Either one will trigger `konira` to
enable profiling.

``py.test`` integration
=======================
``py.test`` is a powerful test runner and testing tool that has a lot of
powerful features. If you have ever tried it, you might miss using it to run
tests. 

If you are combining test cases from Konira with other *regular* unit tests,
you might want to have an aggregated metric (like coverage) when all tests run.
For this reason, there is a ``pytest-konira`` plugin, that allows collection of
Konira tests cases with ``py.test``.

This is a separate package from Konira, so you need to install it with pip::

    pip install pytest-konira

And then you can run tests with::

    py.test --konira
