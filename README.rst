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

It may be useful if one wants to demonstrate created predictive model and
quickly integrate into existing application. Additionally UI is provided for
input data (based on training dataframe) and simple dashboard.

.. image:: https://raw.githubusercontent.com/jettify/mlserve/master/docs/_static/list_models.png
    :alt: mlserve models

.. image:: https://raw.githubusercontent.com/jettify/mlserve/master/docs/_static/one_model.png
    :alt: one model
    
Ideas
-----
**mlsserve** is small using following design based on following ideas:

- Simplicity and ease of use is primary objective.
- Application consists of two processes: IO process that runs HTTP server
  and responsible for fetching and sending data, as well as serve UI, other
  process (worker) is doing CPU intensive work related to predictions
  calculations.


Features
========
* Model predictions serving via RESTful API endpoint.
* Model predictions serving via generated UI.
* Web page to simplify models usage.
* Automatic UI generation to match your input data.
* Simple dashboard for monitoring purposes.


Installation
============

Installation process is simple, just::

    $ pip install git+https://github.com/jettify/mlserve.git

Example
=======

To deploy model just follow following simple steps:

Save your model into pickle file::

    with open('boston_gbr.pkl', 'wb') as f:
        pickle.dump(clf, f)

Use `build_schema` function to build UI representation of pandas dataframe,
and save it as json file file::

    import mlserve

    data_schema = mlserve.build_schema(df)
    with open('boston.json', 'wb') as f:
        json.dump(data_schema, f)

Create configuration file with following format::

    models:
      - name: "boston_regressor"  # url friendly name
        description: "Boston GBR"  # optional model description
        model_path: "boston_gbr.pkl"  # path to your saved model
        data_schema_path: "boston.json"  # path to data representation
        target: "target"  # name of the target column

Serve model::

    $ mlserve -c models.yaml


Thats it, model is available throw REST API, you can test is with curl command::

    $ curl --header "Content-Type: application/json" --request POST
    --data '[{"feature1": 1, "feature2": 2}]'
    http://127.0.0.1:9000/api/v1/models/boston_gradient_boosting_regressor/predict


UI is available via http://127.0.0.1:9000


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
