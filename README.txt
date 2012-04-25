
``uncommitted2`` -- Scan Version Control For Uncommitted Changes
===============================================================

This project was originally created by Brandon Rhodes for SVN &
Mercurial. (http://bitbucket.org/brandon/uncommitted).

Version 2 adds some features:
* Support for checking branches for unpushed commits.
* cronjob for notification

When working on one version-controlled project on my hard drive, I often
flip over quickly to another project to make a quick change.  By the end
of the day I have forgotten about that other change and often find it
months later when I enter that repository again.  I needed a way to be
alerted at the end of each day about any uncommitted changes sitting
around on my system.

Thus was born this "uncommitted2" script: using either your system
*locate(1)* command or by walking a filesystem tree on its own, it will
find version controlled directories and print a report on the standard
output about any uncommitted changes still sitting on your drive.  By
running it from a *cron(8)* job you can make this notification routine.

Running "uncommitted2"
----------------------

By default "uncommitted2" uses the *locate(1)* command to scan for
repositories, which means that it can operate quickly even over very
large filesystems like my home directory::

    $ uncommitted2 ~

But you should **be warned:** because the *locate(1)* database is only
updated once a day on most systems, this will miss repositories which
you have created since its last run.  To be absolutely sure to see all
current repositories, you should instead ask "uncommitted2" to search the
filesystem tree itself.  To do this on your "devel" directory, for
example, you would type this::

    $ uncommitted2 -w ~/devel

Not only will the output of "-w" always be up-to-date, but it is usually
faster for small directory trees.  The default behavior of using
*locate(1)* (which can also be explicitly requested, with "-l") is
faster when the directory tree you are searching is very large.

Should you ever want a list of all repositories, and not just those with
uncommitted changes, you can use the "-v" verbose option::

    $ uncommitted2 -v ~

You can always get help by running "uncommitted2" without arguments or
with the "-h" or "--help" options.

Supported VCs
-------------

At the moment, "uncommitted2" supports:

* `Mercurial`_ (.hg directories)
* `Git`_ (.git directories)
* `Subversion`_ (.svn directories)

I am not opposed to someone contributing code to support Bazaar, or
other more obscure version control systems.  But we should probably keep
"uncommitted2" from ever supporting CVS, because that might imply that it
is still an acceptible system to be using.

It occurs to me that there might already be some version control
abstraction layer that I should be using for this, rather than figuring
out how to run each version control system myself; a quick search of
PyPI suggests that I take a closer look at the `pyvcs`_ project.  Maybe
that can be a useful direction for the next phase of development!

.. _Mercurial: http://mercurial.selenic.com/
.. _Subversion: http://subversion.tigris.org/
.. _Git: http://git-scm.com/
