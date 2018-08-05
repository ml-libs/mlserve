mlserve
=======
.. image:: https://travis-ci.com/jettify/mlserve.svg?branch=master
    :target: https://travis-ci.com/jettify/mlserve
.. image:: https://codecov.io/gh/jettify/mlserve/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jettify/mlserve
.. image:: https://api.codeclimate.com/v1/badges/1ff813d5cad2d702cbf1/maintainability
   :target: https://codeclimate.com/github/jettify/mlserve/maintainability
   :alt: Maintainability
.. image:: https://img.shields.io/pypi/v/mlserve.svg
    :target: https://pypi.python.org/pypi/mlserve

**mlserve** turns your python models into RESTful API, serves web page with
form generated to match your input data.


Features
========
* Model predictions serving via RESTful API endpoint.
* Model predictions serving via generated UI.
* Web page to simplify models usage.
* Automatic UI generation to match your input data.
* Simple dashboard for monitoring purposes.


Supported Frameworks
====================
* Scikit-Learn
* Keras (planning)
* PyTorch (planning)


Requirements
------------

* Python_ 3.6+
* aiohttp_

.. _PEP492: https://www.python.org/dev/peps/pep-0492/
.. _Python: https://www.python.org
.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _asyncio: http://docs.python.org/3.6/library/asyncio.html
.. _uvloop: https://github.com/MagicStack/uvloop
