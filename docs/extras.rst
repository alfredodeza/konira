.. _raises:

Assert Exceptions
=================
*konira* provides a nice way of testing exceptions. The DSL introduces a new
keyword for this purpose: ``raises``.

.. note::
    The addition of the new keyword depends on konira being actually imported.
    If you do not `import konira` your file will raise a NameError.

The ``raises`` keyword allows you to write explicit assertions for exceptions.

The most basic example would be something like this test::

    describe "a test for raised exceptions":

        it "should raise an invalid syntax":
            raises Exception: foo()

What is neat about this way of asserting that something was raised is that all
the code that generates an exception can be placed normally after the `:`.

If you had a function or class that needed a bunch of arguments, it would still
read very natural ::

    it "class would raise an exception":
        raises Exception: MyClass('foo', 'bar')

When an exception is not raised, that test would count as a failed one.

