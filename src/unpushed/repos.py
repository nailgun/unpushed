import os
from subprocess import Popen, PIPE


def ilen(it):
    return sum(1 for i in it)


def mercurial(path, ignore_set, **options):
    """Get statuses of a Mercurial repository."""
    ignore_untracked = options['ignore_untracked']

    process = Popen(('hg', 'st'), stdout=PIPE, cwd=path)
    output = process.stdout.read()
    lines = output.splitlines()
    untracked_count = ilen((line for line in lines if line.startswith(b'?')))
    untracked_only = untracked_count == len(lines)

    touched = bool(lines)
    if ignore_untracked and untracked_only:
        touched = False
    if touched:
        if untracked_only:
            status = 'untracked'
        else:
            status = 'uncommitted'
    else:
        status = 'OK'

    yield dict(
        touched=touched,
        path=path,
        status=status,
        output=output,
    )

    process = Popen(('hg', 'out'), stdout=PIPE, cwd=path)
    output = process.stdout.read()
    lines = []
    for line in output.splitlines():
        if not line.strip():
            continue
        if line.startswith(b'comparing with'):
            continue
        if line.startswith(b'searching for changes'):
            continue
        if line.startswith(b'no changes found'):
            continue
        lines.append(line)
    output = '\n'.join(lines)+'\n'

    touched = bool(lines)
    if touched:
        yield dict(
            touched=touched,
            path=path,
            status='unpushed' if touched else 'OK',
            output=output,
        )


def git(path, ignore_set, **options):
    """Get statuses of a Git repository."""
    ignore_untracked = options['ignore_untracked']

    process = Popen(('git', 'status', '--porcelain'), stdout=PIPE, cwd=path)
    output = process.stdout.read()
    lines = output.splitlines()
    untracked_count = ilen((line for line in lines if line.startswith(b'?')))
    untracked_only = untracked_count == len(lines)

    touched = bool(lines)
    if ignore_untracked and untracked_only:
        touched = False
    if touched:
        if untracked_only:
            status = 'untracked'
        else:
            status = 'uncommitted'
    else:
        status = 'OK'

    yield dict(
        touched=touched,
        path=path,
        status=status,
        output=output,
    )

    # Related commands:
    # git log --branches --not --remotes --simplify-by-decoration --decorate --oneline
    # git branch -v
    # git for-each-ref --format='%(refname)' refs/heads
    process = Popen(('git', 'branch'), stdout=PIPE, cwd=path)
    branches = [br[2:] for br in process.stdout.read().splitlines()]
    for branch in branches:
        process = Popen(('git', 'log', branch, '--not', '--remotes',
                         '--simplify-by-decoration',
                         '--decorate', '--oneline', '--'), stdout=PIPE, cwd=path)
        output = process.stdout.read()
        touched = bool(output)
        yield dict(
            touched=touched,
            path='%s:%s' % (path, branch),
            status='unpushed' if touched else 'OK',
            output=output,
        )


def subversion(path, ignore_set, **options):
    """Get statuses of a Subversion repository."""
    ignore_untracked = options['ignore_untracked']

    process = Popen(('svn', 'st', '-v'), stdout=PIPE, cwd=path)
    output = process.stdout.read()
    lines = []
    for line in output.splitlines():
        if not line.strip():
            continue
        if line.startswith(b'Performing'):
            continue
        status = line[:8]
        filename = line[8:].split(None, 3)[-1]
        ignore_set.add(os.path.join(path, filename))
        if status.strip():
            lines.append(status + filename)
    output = '\n'.join(lines)+'\n'

    untracked_count = ilen((line for line in lines if line.startswith(b'?')))
    untracked_only = untracked_count == len(lines)

    touched = bool(lines)
    if ignore_untracked and untracked_only:
        touched = False
    if touched:
        if untracked_only:
            status = 'untracked'
        else:
            status = 'uncommitted'
    else:
        status = 'OK'

    yield dict(
        touched=touched,
        path=path,
        status=status,
        output=output,
    )
