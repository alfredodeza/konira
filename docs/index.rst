.. rubric:: now with 0 calorie syntactic sugar!

Konira - A Python DSL Testing Framework
=======================================
Konira is a tool that allows you to write minimalistic
descriptions for testing scenarios and unit tests.

It is flexible enough to accommodate Behavioral Driven 
Development as well as traditional Unit Testing. 

It also adds a few neat things to make testing easier.

See :ref:`why` would you ever want to use it if you have
tried UnitTest before.

As a testing tool, it takes testing itself **seriously** and is tested
and verified to work on 

* Python 2.5, 2.6, 2.7, 3.0, 3.1 and 3.2
* PyPy 1.5 and 1.6

Konira's own test suite consists of about 200 tests that run in
about ``0.120s``

It provides a test runner, a dsl and you can optionally use ``py.test``
to run these tests (using the ``pytest-konira`` plugin installed separately).

If you develop with Vim editor, there is also a plugin that will enable
syntax highlighting and running tests from within Vim (see:
https://github.com/alfredodeza/konira.vim)



How does a test case looks like?
------------------------------------

.. highlight:: ruby

::

    describe "a very simple test case for my_module":

        it "has a foo property that is False":
            assert my_module.foo == False


But this is not valid Python!
---------------------------------

I hear you. It is a DSL. All tests need to be prefaced by the ``case_`` word.
As long as that convention is matched the autodiscovery engine will pick up
your DSL test cases.

Since version ``0.1.0`` it is no longer needed to specify an encoding at the
top. Konira tests are now translated on the fly!




fast and readable action in the terminal
--------------------------------------------
Most tests take a mere 0.0007s to run!

.. highlight:: text

::

    $ konira
    
    a very simple test case for my_module
        It has a foo property that is True
    

    All specs passed in 0.000 secs.


Are you sold yet?
---------------------

Head over to :ref:`basic-structure` to get you started right away. The :ref:`commandline` guides 
you on terminal usage and :ref:`advanced-structure` will cover more complex
usage.


The name
------------

*Konira* is one of the names of an ancient Inca God. Konira Wirakocha diguised 
as a traveler in rags. A trickster, a prankster. No one knew who he was, and the 
people he passed called him names. Yet as he walked, he created. With a word he 
made the fields and terraced hillsides. Dropping a reed blossom, he made water flow.

This is a DSL, it looks like Python - it mostly is, but it packs simplicity and makes
testing look good and easy.


Editor Support
--------------
Are you using Vim? You may want to install the konira.vim plugin. It allows you
to run tests form within Vim and get immediate feedback.

It also adds syntax highlighting to your konira tests as soon as you open them!

The plugin can be grabbed from `GitHub <https://github.com/alfredodeza/konira.vim>`_


