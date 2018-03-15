"""The 'unpushed' command-line tool itself."""

import os
import sys
from optparse import OptionParser

from . import scanner

USAGE = '''usage: %prog [options] path [path...]

  Checks the status of all Version Control repositories beneath the paths
  given on the command line.  Any repositories with uncommitted changes
  are printed to standard out, along with the status of the files inside.'''


def main():
    parser = OptionParser(usage=USAGE)
    parser.add_option('-l', '--locate', dest='use_locate', action='store_true',
                      help='use locate(1) to find repositories')
    parser.add_option('-v', '--verbose', action='store_true',
                      help='for each repository print it\'s status')
    parser.add_option('-a', '--all', action='store_true', dest='print_all',
                      help='print every repository whether changed or not')
    parser.add_option('-w', '--walk', dest='use_walk', action='store_true',
                      help='manually walk file tree to find repositories')
    parser.add_option('-t', '--tracked', dest='ignore_untracked', action='store_true',
                      help='ignore untracked files in repositories')
    parser.add_option('-s', '--short', dest='short_info', action='store_true', 
                      help='print short repository status')
    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        exit(2)

    if options.use_locate and options.use_walk:
        sys.stderr.write('Error: you cannot specify both "-l" and "-w"\n')
        exit(2)

    if options.use_walk:
        find_repos = scanner.find_repos_by_walking
    else:
        find_repos = scanner.find_repos_with_locate

    repos = set()

    for path in args:
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            sys.stderr.write('Error: not a directory: %s\n' % (path,))
            continue
        repos.update(find_repos(path))

    repos = sorted(repos)
    for status in scanner.scan_repos(repos, ignore_untracked=options.ignore_untracked):
        if status['touched'] or options.print_all:
            status_char = '*' if status['touched'] else ' '
            if options.short_info:
                print(status_char, os.path.basename(status['path']), status['status'])
            else:
                print(status_char, status['path'], status['status'], '('+status['vcs']+')')
            if options.verbose:
                print(status['output'])


if __name__ == '__main__':
    main()
