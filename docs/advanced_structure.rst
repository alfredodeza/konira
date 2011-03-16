.. _advanced-structure:

Advanced Structure
==================
The more advanced techniques for testing in *Konira* are covered here. If you
need something more basic to get started with try the :ref:`basic-structure`.

*Konira* is very flexible unlike other testing frameworks in Python. Proper
test scenario setups and tear downs are easier to read and control.

This section will cover how these test controlling keywords make testing
easier.


Setting up a Test Scenario
==========================
The setup section has two helper keywords in *Konira*:

 * ``before all``
 * ``before each``

 Each one affects differently how your tests are set before test are run.


before all
----------
``before all`` gets called once before **any** tests are run in a given
scenario.

For example, in the below test case, ``before all`` would be called **once**
before all the tests::

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
the setup stage, we would use ``before each`` in this way::

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
