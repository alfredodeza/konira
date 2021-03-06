.. rubric:: now with 0 calorie syntactic sugar!

Konira - A Python DSL Testing Framework
=======================================
Konira is a tool that allows you to write minimalistic
descriptions for testing scenarios and unit tests.

It is flexible enough to accommodate Behavioral Driven 
Development as well as traditional Unit Testing. 

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


What does a test case look like?
------------------------------------

.. highlight:: ruby

::

    describe "a very simple test case for my_module":

        it "has a foo property that is True":
            assert my_module.foo


But this is not valid Python!
---------------------------------

I hear you. It is a DSL. All tests need to specify the ``konira`` encoding
at the top and they can be executed with the included command line tool.

fast and readable action in the terminal
--------------------------------------------

.. highlight:: text

::

    $ konira
    
    a very simple test case for my_module
        It has a foo property that is True
    

    All specs passed in 0.000 secs.


Are you sold yet?
---------------------

Fork the project and start contributing. 
Full documentation can be found at http://konira.cafepais.com
If you have any ideas or suggestions ping me @alfredodeza

The name
------------

*Konira* is one of the names of an ancient Inca God. Konira Wirakocha diguised 
as a traveler in rags. A trickster, a prankster. No one knew who he was, and the 
people he passed called him names. Yet as he walked, he created. With a word he 
made the fields and terraced hillsides. Dropping a reed blossom, he made water flow.

This is a DSL, it looks like Python - it mostly is, but it packs simplicity and makes
testing look good and easy.


