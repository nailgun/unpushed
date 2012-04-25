"""The 'unpushed-notify' command-line tool."""

import os
import sys
from optparse import OptionParser

from . import scanner

USAGE = '''usage: %prog [options] path [path...]

  Checks the status of all Version Control repositories beneath the paths
  given on the command line.  Notify on OSD if some of them has changes.'''

def here(*args):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *args)

def notify_linux(report):
    import os
    import re
    import getpass
    from subprocess import Popen, PIPE
    import pynotify
    w = Popen(('w', getpass.getuser()), stdout=PIPE).stdout.read().splitlines()[2:]
    displays = set()
    for entry in w:
        display = entry.split(None, 8)[2]
        displays.add(display)
    print displays
    filtered = set()
    for display in displays:
        m = re.match(r'^(:\d+)\.\d+$', display)
        if m:
            root_display = m.group(1)
            if root_display not in displays:
                filtered.add(display)
        else:
            filtered.add(display)
    print filtered
    for display in filtered:
        os.environ['DISPLAY'] = display
        pynotify.init('unpushed-notify')
        icon = 'file://'+here('logo.png')
        n = pynotify.Notification('You have changes in working directory', report, icon)
        n.show()

def main():
    parser = OptionParser(usage=USAGE)
    parser.add_option('-l', '--locate', dest='use_locate', action='store_true',
                      help='use locate(1) to find repositories')
    parser.add_option('-w', '--walk', dest='use_walk', action='store_true',
                      help='manually walk file tree to find repositories')
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
    report = ''
    for status in scanner.scan_repos(repos):
        if status['touched']:
            report += '%s %s (%s)\n' % (status['path'], status['status'], status['vcs'])
    if report:
        if sys.platform.startswith('linux'):
            notify_linux(report)
        else:
            raise NotImplementedError('Notification is not implemented for this system')

if __name__ == '__main__':
    main()
