Pinback - Pinboard Backup Tool
==============================

This is a CLI program for backuping pinboard bookmarks,
with a neat API class implemented.


Installation
------------

pinback requires ``requests`` to be installed::

    pip install requests


Usage
-----

First you need to get your api token from `settings/password
<https://pinboard.in/settings/password>`_, and write it to ``.token`` file::

    $ echo yourtoken > .token

Simple backup, file name will be generated by date::

    $ python pinback.py
    $ ls pinboard*
    pinboard-backup-2015-01-22.xml


Indicate file name::

    $ python pinback.py pinboard-backup-0122.xml


Something Interesting
---------------------

This is an afternoon-tea project which was accomplished in one and a half hours,
from ``Jan 22 14:25:18 2015`` to ``Jan 22 15:45:52 2015``, could be seen as
some sort of effective developing, and remind me of this fantastic `video
<http://youtu.be/E1oZhEIrer4>`_, hope one day I can achieve that :)
