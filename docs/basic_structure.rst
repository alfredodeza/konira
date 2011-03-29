.. _basic-structure:

Basic Structure
===============
Testing with *Konira* is straightforward: you describe a given situation and
then you make small assertions about it.


First test
----------
Let's assume you have a ``foo.py`` file with a ``Foo`` class that has some 
properties and needs some testing. And this class looks like this::

    class Foo(object):

        def bar(self):
            return True

        def foo(self):
            return False

Simple enough, it has a couple of methods that return booleans. How do we test 
that?

In a different file, that should match *Konira's* file naming conventions
(files should start with ``case_``) a test scenario would be like this:

.. highlight:: ruby

::

    # coding: konira

    from foo import Foo


    describe "the Foo class":

        it "has a bar method that always returns True":
            my_module = Foo()
            assert my_module.bar

That single test has a few things going on around it:

 #. Sets the right encoding for the DSL (``# coding: konira``)
 #. Imports the ``Foo`` class
 #. Starts a test scenario where the string describes the test
 #. Starts a unique test about a method in ``Foo``


 If you save your file and run the ``konira`` command in the terminal
 you should see output similar to this:

.. highlight:: text

::
    
    $ konira
    
    the foo class
        It has a bar method that always returns True
    

    All specs passed in 0.000 secs.

Congratulations! You have just written your first test case and it passed. 


Adding more tests
-----------------
Since we have a few more methods in the ``Foo`` module, adding more test cases
is trivial. The complete test file would look like this with all the 
remaining tests:

.. highlight:: ruby

::

    # coding: konira

    from foo import Foo


    describe "the Foo class":

        it "has a bar method that always returns True":
            my_module = Foo()
            assert my_module.bar

        it "has a foo method that always returns False":
            my_module = Foo()
            assert my_module.foo == False


If you run that file again, you should see a few more *green* passing tests
in the terminal:

.. highlight:: text

::

    $ konira
    
    the foo class
        It has a bar method that always returns True
        It has a foo method that always returns False
    

    All 2 specs passed in 0.000 secs.


Failing Tests
-------------
So far we have covered passing tests. But how do you deal with failing
ones?

By default *Konira* suppresses tracebacks and gives you a minimal error
reporting in the terminal. With some command line options you can 
control more output if desired.

Let's see what happens when we add a failing test:

.. highlight:: ruby

::

    describe "some test scenario":

        it "has a property that is true":
            assert 1 == 2

If you run the above code at the command line you would get an output similar 
to this:

.. highlight:: text

::

    $ konira 


    some test scenario
        It has a property that is true

    Failures:
    ---------

    1 ==> AssertionError
    Starts and Ends: /Users/alfredo/python/case_fail.py:6:


    1 spec failed, 1 total in 0.017 secs.


The above output does not have a full traceback on purpose (this is the 
default behavior). But it also provides some extra information that is
useful for debugging: 

 #. Provides a color coded failing description (in red)
 #. Adds a count to the failing tests with the Exception name
 #. Displays the complete file path and file number where the exception occurred.


For more detailed output (that includes a traceback) you need to pass in the 
``-t`` flag to the command line tool::

    $ konira -t


    some test scenario
        It has a property that is true

    Failures:
    ---------

    1 ==> AssertionError
    Starts and Ends: /Users/alfredo/python/case_fail.py:6:
    Assert Diff: '1 == 2'
    E            1 == 2
    Traceback (most recent call last):
      File "/Users/alfredo/python/case_fail.py", line 6, in it_has_a_property_that_is_true
        assert 1 == 2
    AssertionError



    1 spec failed, 1 total in 0.016 secs.


Fixing our small mistake of asserting that one is equal to two, fixes the test,
and we end up having a passing test with green color coded output::

    some test scenario
        It has a property that is true



    All specs passed in 0.000 secs.


Next steps
----------
At this point we have covered how to create the most simple test scenarios
possible to test a class in a different file and we went from some failing
tests to passing tests while controlling terminal output.

There are a few things you might want to look at next if you feel you need some
more advanced examples and *Konira* control:

 * :ref:`advanced-structure`
 * :ref:`commandline-options`

