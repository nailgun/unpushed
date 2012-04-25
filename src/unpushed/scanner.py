import os
import re
from subprocess import Popen, PIPE

from . import repos

class ErrorCannotLocate(Exception):
    """Signal that we cannot successfully run the locate(1) binary."""

globchar = re.compile(r'([][*?])')

def escape(s):
    """Escape the characters special to locate(1) globbing."""
    return globchar.sub(r'\\\1', s)

def find_repos_with_locate(path):
    """Use locate to return a sequence of (path, vcsname) pairs."""
    patterns = []
    for dotdir in DOTDIRS:
        # Escaping the slash (using '\/' rather than '/') is an
        # important signal to locate(1) that these glob patterns are
        # supposed to match the full path, so that things like
        # '.hgignore' files do not show up in the result.
        patterns.append(r'%s\/%s' % (escape(path), escape(dotdir)))
        patterns.append(r'%s\/*/%s' % (escape(path), escape(dotdir)))
    process = Popen([ 'locate', '-0' ] + patterns, stdout=PIPE)
    paths = process.stdout.read().strip('\0').split('\0')
    return [ (os.path.dirname(p), DOTDIRS[os.path.basename(p)]) for p in paths
             if not os.path.islink(p) and os.path.isdir(p) ]

def find_repos_by_walking(path):
    """Walk a tree and return a sequence of (path, vcsname) pairs."""
    repos = []
    DOTDIRS_items = DOTDIRS.items()
    for dirpath, dirnames, filenames in os.walk(path):
        for dotdir, vcsname in DOTDIRS_items:
            if dotdir in dirnames:
                repos.append((dirpath, vcsname))
    return repos


DOTDIRS = {
    '.hg': 'Mercurial',
    '.git': 'Git',
    '.svn': 'Subversion',
}

STATUS_FUNCTIONS = {
    'Mercurial': repos.mercurial,
    'Git': repos.git,
    'Subversion': repos.subversion,
}

def scan_repos(repos):
    """Given a repository list [(path, vcsname), ...], scan each of them."""
    ignore_set = set()
    for path, vcsname in repos:
        if path in ignore_set:
            continue
        get_statuses = STATUS_FUNCTIONS[vcsname]
        for status in get_statuses(path, ignore_set):
            status['vcs'] = vcsname
            yield status
