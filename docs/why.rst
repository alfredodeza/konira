.. _why:

Why would I use this instead of Unittest?
=========================================
This is a very valid question. Unittest is the standard way
of testing in Python, it is recommended by almost all developers
that believe in proper testing workflows.

So why use a DSL?

The tl;dr; answer is: because it is easier to read, easier to
implement and easier to use.


Easier to read
--------------
The most simple example for readability in comparison to regular
unittest is when you want to verify when an `Exception` was raised 
or not.

If there is a `foo` function that raises an exception when a couple
of wrong arguments are passed in, this is how it would compare with
both tools.

Unittest solves that problem like this::

    class MyTestClass(unittest.TestCase):

        def test_a_call_that_raises_an_exception(self):
            self.assertRaises(Exception, foo, bad_arg1, bad_arg2)


And this is how it looks in konira:

.. highlight:: konira

::

    describe "my class":

        it "raises an exception when foo is called":
            raises Exception: foo(bad_arg1, bad_arg2)


The konira way of verifying an assertion just feels more natural than
breaking the callable into the name and the arguments.

It is readable **right away** and because it is readable it is easier
to keep writing and using tests like the one above.


Easier to implement
-------------------
And by *implementation* we mean it is easier to get started writing tests. The
whole API in unittest is based upon methods that accept values so that it can
compare them and assert certain interactions.

With Konira everything is just an assert!

This philosophy of just using assert is based on how ``py.test`` does things.
If you are just using assert you have just learned the whole API! Which makes
most of the following methods from unittest irrelevant (as everything is doable
with assert):

 * self.assertEqual
 * self.assertEquals
 * self.assertAlmostEqual
 * self.assertAlmostEquals
 * self.assertFalse
 * self.assertTrue
 * self.assertNotEqual
 * self.assertNotEquals


Easier to use
-------------
When you start using unittest you need to think about the test runner. This is
an important piece of the puzzle since unittest does not provide a *standard*
way of running your tests via auto-discovery or any other kind of niceties the
most popular test runners provide.

Chances are that if you are using a popular test runner you are already *not*
being 100% pure unittest because you might be relying on helpers provided by
those same test runners.

An example of those helpers are the "skip if" decorators to help the test
runner decide if it needs to skip a test given some reason.

*Konira* already packs such a feature and almost every other feature popular
test runners offer, like:

 * fail fast
 * stdout and stderr buffering 
 * skip if as special methods
 * better (re-evaluated) traceback output
 * auto discovery
 * method and class matching for tests


Although we are considering adding a ``py.test`` plugin for konira, you do not
need to decide about the test runner right away since it is already there ready
to be used. It packs the most necessary tools you need to get tests running.


