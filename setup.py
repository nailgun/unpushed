from setuptools import setup, find_packages

setup(
    name = 'uncommitted2',
    version = '1.2',
    description = u'Scan Version Control For Uncommitted Changes',
    long_description = u'Originally Created by Brandon Craig Rhodes\n'
        u'Forked version with Git support by George Eapen\n'
        u'Version 2 fork by Dmitry Bashkatov',
    author = 'Dmitry Bashkatov',
    author_email = 'dbashkatov@gmail.com',
    url = 'http://github.com/nailgun/uncommitted2/',
    classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Console', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Version Control',
        'Topic :: Utilities',
    ],
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    include_package_data = True,
    install_requires = [],
    entry_points = '[console_scripts]\nuncommitted2 = uncommitted2.command:main\n',
)
