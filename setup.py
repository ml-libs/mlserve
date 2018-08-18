import os
import re
import sys
from setuptools import setup, find_packages


PY_VER = sys.version_info

if not PY_VER >= (3, 5):
    raise RuntimeError('mlserve does not support Python earlier than 3.6')


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


install_requires = [
    'aiohttp>=3.0.0',
    'pandas',
    'jsonschema',
    'trafaret',
    'pyyaml',
]
extras_require = {}


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__),
                           'mlserve', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            msg = 'Cannot find version in mlserve/__init__.py'
            raise RuntimeError(msg)


classifiers = [
    'License :: OSI Approved :: Apache Software License',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Operating System :: POSIX',
    'Development Status :: 2 - Pre-Alpha',
    'Framework :: AsyncIO',
]


setup(name='mlserve',
      version=read_version(),
      description=('mlserve -- turns python model into RESTful API'
                   ' with automatically generated UI.'),
      long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
      install_requires=install_requires,
      classifiers=classifiers,
      platforms=['POSIX'],
      author='Nikolay Novik',
      author_email='nickolainovik@gmail.com',
      url='https://github.com/jettify/mlserve',
      download_url='https://pypi.python.org/pypi/mlserve',
      license='Apache 2',
      packages=find_packages(),
      entry_points={'console_scripts': ['mlserve = mlserve.main:main']},
      extras_require=extras_require,
      keywords=['mlserve', 'serving', 'aiohttp'],
      zip_safe=True,
      include_package_data=True)
