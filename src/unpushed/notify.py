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


def notify_osx(reports):
    from AppKit import NSImage
    from Foundation import NSUserNotification
    from Foundation import NSUserNotificationCenter
    from Foundation import NSUserNotificationDefaultSoundName
    for report in reports:
        notification = NSUserNotification.alloc().init()
        notification.setTitle_("%s %s changes" % (report['status'].title(), report['vcs'].lower()))
        notification.setInformativeText_(report['path'])
        image = NSImage.alloc().initByReferencingFile_(here('logo.png'))
        # See http://stackoverflow.com/questions/24923979/nsusernotification-customisable-app-icon
        # Unfortunately I can't seem to get it to work with PyObjC
        # notification.setValue_forKey_(image, "_identityImage")
        notification.setIdentifier_(report['path'])
        notification.setSoundName_(NSUserNotificationDefaultSoundName)
        center = NSUserNotificationCenter.defaultUserNotificationCenter()
        center.deliverNotification_(notification)


def notify_linux(reports):
    import os
    import re
    import getpass
    from subprocess import Popen, PIPE
    import pynotify

    message = ''
    for report in reports:
        message += '%s %s (%s)\n' % (status['path'], status['status'], status['vcs'])
    w = Popen(('w', getpass.getuser()), stdout=PIPE).stdout.read().splitlines()[2:]
    displays = set()
    for entry in w:
        display = entry.split(None, 8)[2]
        displays.add(display)
    filtered = set()
    for display in displays:
        m = re.match(r'^(:\d+)\.\d+$', display)
        if m:
            root_display = m.group(1)
            if root_display not in displays:
                filtered.add(display)
        else:
            filtered.add(display)
    for display in filtered:
        os.environ['DISPLAY'] = display
        pynotify.init('unpushed-notify')
        icon = 'file://'+here('logo.png')
        n = pynotify.Notification('You have changes in working directory', message, icon)
        n.show()


def main():
    parser = OptionParser(usage=USAGE)
    parser.add_option('-l', '--locate', dest='use_locate', action='store_true',
                      help='use locate(1) to find repositories')
    parser.add_option('-w', '--walk', dest='use_walk', action='store_true',
                      help='manually walk file tree to find repositories')
    parser.add_option('-t', '--tracked', dest='ignore_untracked', action='store_true',
                      help='ignore untracked files in repositories')
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
    reports = []
    for status in scanner.scan_repos(repos, ignore_untracked=options.ignore_untracked):
        if status['touched']:
            reports.append(status)
    if len(reports) > 0:
        if sys.platform.startswith('linux'):
            notify_linux(reports)
        elif sys.platform.startswith('darwin'):
            notify_osx(reports)
        else:
            raise NotImplementedError('Notifications not implemented for %s' % (sys.platform))


if __name__ == '__main__':
    main()
