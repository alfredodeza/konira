.. _basic-structure:

Basic Structure
===============
The most basic aspects of test structure are covered here. If you are looking
for something more advanced, you need to go for the :ref:`advanced-structure` 
section.

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
(files should start with ``case_``) a test scenario would be like this::

    # coding: konira

    from foo import Foo


    describe "the Foo class":

        it "has a bar method that always returns True":
            my_module = Foo()
            assert my_module.bar

That single test has a few things going on around it:

 # Sets the right encoding for the DSL (``# coding: konira``)
 # Imports the ``Foo`` class
 # Starts a test scenario where the string describes the test
 # Starts a unique test about a method in ``Foo``


 If you save your file and run the ``konira`` command in the terminal
 you should see output similar to this::

    
    $ konira
    
    the foo class
        It has a bar method that always returns True
    

    All specs passed in 0.000 secs.

Congratulations! You have just written your first test case and it passed. 


Adding more tests
-----------------
Since we have a few more methods in the ``Foo`` module, adding more test cases
is trivial. The complete test file would look like this with all the 
remaining tests::


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
in the terminal::


    $ konira
    
    the foo class
        It has a bar method that always returns True
        It has a foo method that always returns False
    

    All 2 specs passed in 0.000 secs.

