.. rubric:: now with 0 calorie syntactic sugar!

Konira - A Python DSL Testing Framework
=======================================
Konira is a tool that allows you to write minimalistic
descriptions for testing scenarios and unit tests.

It is flexible enough to accommodate Behavioral Driven 
Development as well as traditional Unit Testing. 



How does a test case looks like?
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

Head over to :ref:`getting-started` guide and see what other goodness this
testing tool packs.


The name
------------

*Konira* is one of the names of an ancient Inca God. Konira Wirakocha diguised 
as a traveler in rags. A trickster, a prankster. No one knew who he was, and the 
people he passed called him names. Yet as he walked, he created. With a word he 
made the fields and terraced hillsides. Dropping a reed blossom, he made water flow.

This is a DSL, it looks like Python - it mostly is, but it packs simplicity and makes
testing look good and easy.


