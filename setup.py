from os import path
from codecs import open
from setuptools import setup, find_packages


_NAME = 'frangidoc'
_VERSION = '2.0.2'
_DESCRIPTION = 'Generate markdown from Python sources (reST based)'
_URL = 'https://github.com/MrFrangipane/frangidoc'
_AUTHOR = 'Valentin Moriceau'
_AUTHOR_EMAIL = 'valentin.moriceau@free.com'
_KEYWORDS = 'documentation markdown docstring reST'
_CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Topic :: Software Development :: Documentation',
    'Operating System :: Microsoft',
    'Operating System :: POSIX'
]


_here = path.abspath(path.dirname(__file__))

with open(path.join(_here, 'README.md'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

with open(path.join(_here, "requirements.txt")) as requirements_file:
    requirements = requirements_file.readlines()

dependency_links = []
install_requires = []

for item in requirements:
    if item.startswith('git+'):
        dependency_links.append(str(item))
        install_requires.append(item.split("/")[-1].split(".git")[0])
    else:
        install_requires.append(str(item))

setup(
    name=_NAME,
    version=_VERSION,
    description=_DESCRIPTION,
    long_description=long_description,
    url=_URL,
    author=_AUTHOR,
    author_email=_AUTHOR_EMAIL,
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    dependency_links=dependency_links,
    include_package_data=True,
    classifiers=_CLASSIFIERS,
    keywords=_KEYWORDS
)
