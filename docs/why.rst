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


And this is how it looks in konira::


    describe "my class":

        it "raises an exception when foo is called":
            raises Exception: foo(bad_arg1, bad_arg2)


The konira way of verifying an assertion just feels more natural than
breaking the callable into the name and the arguments.

It is readable **right away** and because it is readable it is easier
to keep writing and using tests like the one above.


Easier to implement
