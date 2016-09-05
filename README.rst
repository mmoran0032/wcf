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
requires the user to obtain a username and password from the WCF to proceed.

Once you have access, create a ``credentials.json`` file in the same directory
you are working in as follows::

    {
        "Username": "user",
        "Password": "something+else"
    }

Basic usage is as follows::

    import wcf
    t = wcf.WCF()
    t.load_and_connect()


Unofficial API
--------------

I've written a basic API to pull the box score data from the WCF:
``wcf_parsing.py``. Right now, it's a basic loading and converting API for just
the box scores, so I lose or don't pull information about the specific players
on the team, the location or venue, the dates it was played, or even the gender
of the athletes. I will have to pull that stuff eventually (into
``Tournament``), but for now raw numbers seem OK. The others may require
another round of exploration.

Requires ``bs4`` (Beautiful Soup).

Usage is simple::

    from wcf import wcf_parsing as wcfp
    t = wcfp.Tournament(tournamentID)
    t.load_all_games()

    final = t.games[-1]
    print(final.teams[final.winner])

From this starting point, a lot of the "business logic" that I put into the
previous two notebooks/scripts is within this module. The aggregate data part
is still another layer on top of the access, but this should help for batch
processing.
