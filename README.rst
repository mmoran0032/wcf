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
conventions. I am implementing this access method in ``wcf.py``, which only
requires the user to obtain a user name and password from the WCF to proceed.

Once you have access, create a ``credentials.json`` file in the same directory
you are working in as follows::

    {
        "Username": "user",
        "Password": "something+else"
    }

You can create your connection with::

    import wcf
    t = wcf.WCF()
    t.load_and_connect()
    # or
    t2 = wcf.WCF(connect=True)

Your credentials can be in a different location that your project directory.
Specify that with::

    t = wcf.WCF(cred_file='path/to/file.json')
