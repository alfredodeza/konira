import sys

# Python3 needs this
if sys.version < '3':
    from distutils.core import setup
    extra = dict()
else:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup
    extra = {'use_2to3':True}

scripts = ['bin/konira']

if sys.platform == 'win32':
    scripts.append('bin/konira.bat') 

setup(
    name             = "konira",
    version          = "0.2.1",
    packages         = ['konira', 'konira.ext'],
    scripts          = scripts,
    author           = "Alfredo Deza",
    author_email     = "alfredodeza [at] gmail.com",
    description      = "A DSL Testing Framework for nicer, (beautiful!) readable BDD tests",
    license          = "MIT",
    keywords         = "test, readable, testrunner, bdd",
    classifiers      = [
                        'Development Status :: 4 - Beta',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: MIT License',
                        'Topic :: Software Development :: Build Tools',
                        'Topic :: Software Development :: Libraries',
                        'Topic :: Software Development :: Testing',
                        'Topic :: Utilities',
                        'Operating System :: MacOS :: MacOS X',
                        'Operating System :: Microsoft :: Windows',
                        'Operating System :: POSIX',
                        'Programming Language :: Python :: 2.5',
                        'Programming Language :: Python :: 2.6',
                        'Programming Language :: Python :: 2.7',
                        'Programming Language :: Python :: 3.0',
                        'Programming Language :: Python :: 3.1',
                        'Programming Language :: Python :: 3.2',
                      ],
    **extra
)
