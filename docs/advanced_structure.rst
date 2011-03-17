.. _advanced-structure:

Advanced Structure
==================
The more advanced techniques for testing in *Konira* are covered here. If you
need something more basic to get started with try the :ref:`basic-structure`.

*Konira* is very flexible unlike other testing frameworks in Python. Proper
test scenario setups and tear downs are easier to read and control.

This section will cover how these test controlling keywords make testing
easier.


Setting Up 
==========
The setup section has two helper keywords in *Konira*:

 * ``before all``
 * ``before each``

Each one affects differently how your tests are set **before** a test run.


before all
----------
``before all`` gets called once before **any** tests are run in a given
scenario.

For example, in the below test case, ``before all`` would be called **once**
before all the tests:

.. highlight:: ruby

::

    describe "a testing scenario":

        before all:
            self.string = "a very long result string"

        it "compares strings":
            assert "very" in self.string

        it "verifies that bar is not in the string":
            assert "bar" not in self.string


In the above code, ``before all`` was called **once** before all the tests were
run and in turn it made the actual tests extremely readable. ``before all`` is
very useful in cases like that, where the actual value is not meant to change
with tests.

For values or attributes that get affected by tests, you may want to use
``before each``.


before each
-----------
This helper method, is called before every test in a test scenario. It is very
useful when you have values or attributes that may change or get altered in
some way by other tests.
Setting a ``before each`` method, ensures that the values are always the same.

If we had a scenario where the tests keep changing the value of anything in
the setup stage, we would use ``before each`` in this way:

.. highlight:: ruby

::

    describe "a testing scenario":

        before each:
            self.value = True

        it "changes a value to False":
            self.value = False
            assert self.value == False

        it "changes a value to a string":
            self.value = "a string"
            assert self.value == "a string"

        it "verifies that value is always True":
            assert self.value


In the above test, we changed the value of ``self.value`` on almost every test,
but this value was *reset* back before each one of them was run.

``before each`` can be really meaningful if you need to create files, or remove
them. Or even if you need to make sure certain things are set before any (and
all) tests are run.


Cleaning Up
===========
In the cleanup phase, *Konira* has two helpers that allow you to fine tune
actions after a test (or tests) have been completed. These are:

 * ``after all``
 * ``after each``

These calls are always made **after** one or all the tests in a given scenario
depending on the helper selected.


after all
---------
``after all`` is a *clean up* helper. It allows you to perform actions after all of
the tests in your test scenario are run.

For example, if your tests have created a file and you need to make
sure it gets removed from the system after all the tests in a scenario are run, then
you would call ``after all``. The way it is used in a scenario is as follows:

.. highlight:: ruby

::
    
    describe "a testing scenario":

        after all:
            os.remove('/tmp/foo.txt')

        it "does some filesystem stuff":
            f = open('/tmp/foo.txt')
            f.write('foo!').close()
            assert os.path.isfile('/tmp/foo.txt')


In the above case, ``after all`` gets called only once after all tests are finished,
to perform any actions it needs to do.


after each
----------
This helper is similar to ``after all`` but it differs in the sense that it is called
every single time a test has completed (even if such test fails).

The syntax is also similar, and would be (from the example above) like so:

.. highlight:: ruby

::

    describe "a testing scenario":

        after each:
            os.remove('/tmp/foo.txt')

        it "does some filesystem stuff":
            f = open('/tmp/foo.txt')
            f.write('foo!').close()
            assert os.path.isfile('/tmp/foo.txt')


The control that ``after each`` gives your test case is more precise and it is applied
for all the tests in your scenario.


Controlling Skips
=================
*Konira* allows you to skip certain tests when some predetermined conditions apply.
It is very common to have situations where depending on your environment you want
to run a subset of tests.

With other testing tools, you need to specify global environments or globally 
accessible values but with *Konira* you can define all the logic you want in
any fashion you may need.

skip if
-------
``skip if`` is a helper that when defined, allows you to put code that when 
evaluated **without** an Exception being raised it will make all the tests in
a scenario to be skipped.


A valid example that would make the whole set of tests in a scenario to be skipped
would look like this:

.. highlight:: ruby

::

    import sys
    
    describe "a testing scenario":

        skip if:
            sys.platform == 'linux2'

        it "changes a value to False":
            assert some_value == False

If the above code was run in a Linux operating system, any tests that where included
in that scenario, would be skipped.

The *whole* scenario would be skipped!

In the case that the code was not run on a Linux OS, the ``skip if`` would raise an 
exception that would be catch by *Konira* and tests would all run.

If a ``skip if`` doesn't evaluate correctly (raising an exception) it does **not** count
as an error or a failure. It simply ignores the exception and execute your tests.
