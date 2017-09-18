wcf -- World Curling Federation Data Wrangler
=============================================

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
to the file to ``WCF.load_and_connect()`` as an argument.


Example Usage
-------------

As a quick example, let's look at the final game from the World Men's Curling
Championship 2016 in Basel, SUI::

    import wcf

    conn = wcf.WCF()
    conn.load_and_connect()
    draws = conn.get_draws_by_tournament(555)

    final = wcf.Game(draws[-1])
    final.convert()
    print(final)


Testing
-------

The test suite can be run with::

    py.test --cov=wcf
