Contributing
============

Setting Development Environment
-------------------------------

.. _GitHub: https://github.com/jettify/mlserve

Thanks for your interest in contributing to ``mlserve``, there are multiple
ways and places you can contribute, help on on documentation and tests is very
appreciated.

To setup development environment, fist of all just clone repository::

    $ git clone git@github.com:jettify/mlserve.git

Create virtualenv with python3.7 (python 3.6 also supported). For example
using *virtualenvwrapper* commands could look like::

   $ cd mlserve
   $ mkvirtualenv --python=`which python3.7` mlserve


After that please install libraries required for development::

    $ pip install -r requirements-dev.txt
    $ pip install -e .


Running Tests
-------------
Congratulations, you are ready to run the test suite::

    $ make cov

To run individual test use following command::

    $ py.test -sv tests/test_utils.py -k test_name



Reporting an Issue
------------------
If you have found an issue with `mlserve` please do
not hesitate to file an issue on the GitHub_ project. When filing your
issue please make sure you can express the issue with a reproducible test
case.

When reporting an issue we also need as much information about your environment
that you can include. We never know what information will be pertinent when
trying narrow down the issue. Please include at least the following
information:

* Version of `mlserve` and `python`.
* Versions of installed python libraries `pip freeze`.
* Platform you're running on (OS X, Linux).

.. _Docker: https://docs.docker.com/engine/installation/
