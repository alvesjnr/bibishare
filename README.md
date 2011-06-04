Bibishare
=========

Bibbishare is a system for sharing informations about bibliographic publications.

Bibishare provides also a Wiki space and a space for place comments.

Installing
----------

Just clone this repository and run:

	$python setup.py develop

It will automatically download and install all python-dependencies.

For pushing couch view (located at couchapp folder) you must have installed
couchapp in your system. Once with couchapp installed, in couchapp folder
run:

	$couchapp push bibishare


Running
_______

For running with paster, just run:

	$paster serve development.ini
