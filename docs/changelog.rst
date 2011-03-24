.. _changelog:

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
