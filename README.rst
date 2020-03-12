|Build Status| |PyPI Version| |Python Versions|

xapian-bindings
===============

**NOTE: This package is not yet fully functional!**

xapian-bindings is a meta-package to simplify installation of the `xapian-bindings <https://xapian.org/download>`_ extension
for Python. It determines the version of ``xapian-bindings`` to use based on the version of `xapian-core <https://xapian.org/download>`_ installed;
downloads and extracts the source code; then runs ``./configure``, ``make`` and ``make install``.

This project is not affiliated with the `Xapian <https://xapian.org/>`_ project in any way.

Installation
------------

1. Ensure you have essential build & development tools installed on your system.
2. Ensure you have ``xapian-core`` installed via your system package manager or source tarball.
3. Run ``pip install --no-cache-dir xapian-bindings``.
4. Verify installation by running ``python -c "import xapian; print(xapian.__version__)"``.

Todos
-----

* Prevent building binary package (wheel) and/or using cached wheel.
* Record files installed under ``site-packages/xapian/``.
* Uninstall files under ``site-packages/xapian/``.
* Add ``.travis.yml``.


.. |Build Status| image:: http://img.shields.io/travis/ninemoreminutes/xapian-bindings.svg
   :target: https://travis-ci.org/ninemoreminutes/xapian-bindings
.. |PyPI Version| image:: https://img.shields.io/pypi/v/xapian-bindings.svg
   :target: https://pypi.python.org/pypi/xapian-bindings
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/xapian-bindings.svg
   :target: https://pypi.python.org/pypi/xapian-bindings
