import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES')).read()

requires = ['pyramid', 'WebError', 'SQLAlchemy', 'couchdbkit', 'isisdm', 'pyramid_zcml', 
            'pystache', 'textile', 'pycrypto', 'pyramid_handlers', 'Woosh']

setup(name='bibishare',
      version='0.2',
      description='bibishare',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="bibishare",
      entry_points = """\
      [paste.app_factory]
      main = bibishare:main
      """,
      paster_plugins=['pyramid'],
      )

