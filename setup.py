from setuptools import setup, find_packages

setup(
    name = 'unpushed',
    version = '1.0',
    description = u'Scan version control for uncommitted and unpushed changes',
    long_description = u'Originally Created by Brandon Craig Rhodes\n'
        u'Forked version with support of unpushed '
        u'branches and notification.',
    author = 'Dmitry Bashkatov',
    author_email = 'dbashkatov@gmail.com',
    url = 'http://github.com/nailgun/unpushed/',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Version Control',
        'Topic :: Utilities',
    ],
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    package_data = {'': ['*.png']},
    include_package_data = True,
    install_requires = [],
    entry_points = '[console_scripts]\n'
        'unpushed = unpushed.command:main\n'
        'unpushed-notify = unpushed.notify:main\n',
)
