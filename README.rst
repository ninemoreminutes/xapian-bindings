|Build Status| |PyPI Version| |Python Versions|

xapian-bindings
===============

xapian-bindings is a meta-package to simplify installation of the ``xapian-bindings`` extension
for Python. It determines the version to use based on the version of ``xapian-core`` installed;
downloads and extracts the source code; then runs ``./configure``, ``make`` and ``make install``.

This project is not affiliated with the Xapian project in any way.

Installation
------------

1. Ensure you have build/development tools installed on your system.
2. Ensure you have ``xapian-core`` installed via your system package manager or source tarball.
3. Run ``pip install xapian-bindings``.
4. Verify installation by running ``python -c "import xapian"``.


.. |Build Status| image:: http://img.shields.io/travis/ninemoreminutes/xapian-bindings.svg
   :target: https://travis-ci.org/ninemoreminutes/xapian-bindings
.. |PyPI Version| image:: https://img.shields.io/pypi/v/xapian-bindings.svg
   :target: https://pypi.python.org/pypi/xapian-bindings
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/xapian-bindings.svg
   :target: https://pypi.python.org/pypi/xapian-bindings
