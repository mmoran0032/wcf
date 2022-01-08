Not actively maintained here. See `Gitlab <https://gitlab.com/mmoran0032/wcf>`_ for details.

wcf -- World Curling Federation Database Interface
==================================================

*Note: this package is not officially endorsed or supported by the WCF*

Pull tournament and game data from the
`World Curling Federation's <http://worldcurling.org/>`__
`results site <http://results.worldcurling.org>`__, using ``requests``.
Requires an active and stable internet connection.

This package was originally created to supplement my needs of pulling the data
while I was waiting for official API access. It also includes accessing the
results database through official means.


API
---

Official access to the WCF's results database must be obtained prior to using
the official API to access the information. Access follows standard REST
conventions. Create a ``credentials.json`` file as follows::

    {
        "Username": "user",
        "Password": "something+else"
    }

The file can either be placed in the same directory, or you can pass the path
to the file to ``WCF.API()`` as an argument. The data is returned
as a formatted JSON response, as each use case of the data could require
different portions of the response. Since development was directed by what *I*
needed, not the entire API is implemented.

Usage is as follows::

    import wcf

    conn = wcf.API().connect()
    # alternatively:
    # conn = wcf.API('credentials/wcf.json')
    # conn.connect()
    draws = conn.get_draws_by_tournament(555)


Testing
-------

Testing requires that you have a credentials file located in this directory.
The test suite can be run with::

    py.test --cov=wcf
