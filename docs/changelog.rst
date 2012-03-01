.. _changelog:

0.3.2
-----
 * Making Konira a zip archive as it breaks on other Python versions
   if we continue down the road of tar.gz

0.3.1
-----
 * Fixes an issue were relative or same-level imports would not work.
 * Updates the documentation from a fork. Weeeeee

0.3.0
-----
 * Even more speed improvements refactoring the tokenizer module by creating
   a dispatcher.
 * Better support for the pytest-konira plugin.
 * Introduces the ``let`` syntax for better (inexpensive) attributes at setup
   time.

0.2.1
-----
 * Create Windows support by including a bat file and removing coloring output
   in the terminal.
 * Increase the speed a bit with some refactoring.
 * Add a few command line switches to get finer granular collection of test
   cases.
 * Adds support for py.test so that the pytest-konira plugin can hook into
   konira and execute tests.

0.2.0
-----
 * Adds a ``--debug`` file that avoids traceback cleanup.
 * Adds 2 collecting regexes options for collecting files other than
   `case_*.py``
 * Better MS Windows support with removal of colored output and addition of
   bat script at installation time.

0.1.1
-----
 * Removes encoding (yay!)
 * adds some utilities that help other test runner plugins

0.0.7
-----
 * Profiling added
 * Removes reporting capabilities from the Runner


0.0.6
-----
 * Bug-fix release
 * The `konira.ext` module was not included in the sdist (Mark McClain)


0.0.5
-----
 * Adds coverage capabilities.
 * Adds `--show-missing` to the coverage options
 * Modifies heavily how options and arguments are parsed at the CLI


0.0.4
-----
 * Adds support for Python2.5 by fixing issues - mainly about the
   with-statement (Gustavo Picon)
 * Fixes a problem of *not* capturing stderr when the cli runs.


0.0.3
-----
 * The `raises` keyword needs to `import konira` explicitly.
 * Adds two flags for the CLI to show the current version
 * When there are errors or failures, it calls sys.exit(2) (Gustavo Picon)
 * Fixes SyntaxError descriptions when an error is raised
 * Adds tox support (Gustavo Picon)


0.0.2
-----
 * When there is a syntax error in a Konira, it is no longer pruned but
   re-raised.


0.0.1
-----
 * Initial release
 * Constructor support: before each, before all, after each, after all 
 * skip if support
 * basic functional command line options
