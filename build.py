from pybuilder.core import use_plugin, init, task, depends, Author

use_plugin('python.core')
use_plugin('python.unittest')
use_plugin('python.install_dependencies')
use_plugin('python.flake8')
use_plugin('python.coverage')
use_plugin('python.distutils')


name = 'simplesvn'
summary = 'High level interface with a basic set of methods using pysvn'
description = """This module is intended for the use in packaging systems,
which triggers a new build on every commit using the post-commit hook."""
license = 'Apache License 2.0'
authors = [Author('Stefan Neben', "stefan.neben@mailfoo.net")]
url = 'https://github.com/sneben/python-simplesvn/'
version = '0.1'
default_task = ['clean', 'analyze', 'package']


@init
def set_properties(project):
    project.build_depends_on('unittest2')
    project.build_depends_on('mock')
    # The pysvn package is not available via "pip install". You need to
    # manually install the version provided by your distribution.
    # project.depends_on('pysvn')


@task
@depends('prepare')
def build_directory(project):
    print project.expand_path("$dir_dist")
