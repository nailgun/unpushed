import os
from subprocess import Popen, PIPE

def mercurial(path, ignore_set):
    """Get statuses of a Mercurial repository."""
    process = Popen(('hg', 'st'), stdout=PIPE, cwd=path)
    output = process.stdout.read()
    touched = bool(output)
    yield dict(
        touched=touched,
        path=path,
        status='uncommitted' if touched else 'OK',
        output=output,
    )

def git(path, ignore_set):
    """Get statuses of a Git repository."""
    process = Popen(('git', 'status', '--porcelain'), stdout=PIPE, cwd=path)
    output = process.stdout.read()
    touched = bool(output)
    yield dict(
        touched=touched,
        path=path,
        status='uncommitted' if touched else 'OK',
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

def subversion(path, ignore_set):
    """Get statuses of a Subversion repository."""
    process = Popen(('svn', 'st', '-v'), stdout=PIPE, cwd=path)
    output = process.stdout.read()
    lines = []
    for line in output.splitlines():
        if not line.strip():
            continue
        if line.startswith('Performing'):
            continue
        status = line[:8]
        filename = line[8:].split(None, 3)[-1]
        ignore_set.add(os.path.join(path, filename))
        if status.strip():
            lines.append(status + filename)
    touched = bool(lines)
    yield dict(
        touched=touched,
        path=path,
        status='uncommitted' if touched else 'OK',
        output='\n'.join(lines)+'\n',
    )
