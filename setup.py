from setuptools import setup, find_packages
setup(
    name         = "jargon",
    version      = "0.0.1",
    packages     = find_packages(),
#    scripts      = ['jargon.py'],
    entry_points = {'console_scripts':['jargon   = jargon:main']},
    author       = "Alfredo Deza",
    author_email = "alfredodeza [at] gmail.com",
    description  = "Nicer tests",
    license      = "MIT",
    keywords     = "test, readable, testrunner"

)

