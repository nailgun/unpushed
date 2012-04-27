import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.abspath(os.path.dirname(__file__)), fname)).read()

setup(
    name = 'unpushed',
    version = '1.0.2',
    description = u'Scan version control for uncommitted and unpushed changes',
    long_description = read('README.rst'),
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
