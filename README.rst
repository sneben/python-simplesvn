=========
simplesvn
=========

Overview
========
High level interface with a basic set of methods using pysvn. This module is
intended for the use in packaging systems, which triggers a new build on
every commit using the ``post-commit`` hook.

Installation
============
To build the project follow these steps:

.. code-block:: console

   $ virtualenv venv
   $ source venv/bin/activate
   $ pip install pybuilder
   $ pyb install_dependencies
   $ pyb -v

The generated install source can be found in ``target/dist/simplesvn-0.1/``.
Do what ever you want with the ``setup.py``.

Methods
=======
list
----
Returns a list of files and directories located at the given source.

:Parameter: *source*

URL of the svn location which should be listed. For example:
``https://svn.example.com/repo/dir``.

:Parameter: *recursive=False*

Do an recursive listing on the given location. Default is ``False``.

get_changed_paths
-----------------
Build a summary list of all changed files under the given source.

:Parameter: *source*

URL of the svn location which should be probed. For example:
``https://svn.example.com/repo/``.

:Parameter: *start=1*

Always add entries with a path count greater than the given start value. Else
entries which were **deleted** are not added to the list. Default is **1**.

get_file_content
----------------
Read out the content of the given file directly from remote location, whithout
the need of a checkout.

:Parameter: *source*

URL of the files svn location. For example:
``https://svn.example.com/repo/file``.

exists
------
Check if the given svn ressource exists. Returns ``True`` if exist and
``False`` if not.

:Parameter: *source*

URL of the ressources svn location. For example:
``https://svn.example.com/repo/file``.

export
------
Export files or directories and return the revision number. Returns a list
including the revision number and the commit message (``[revision, message]``).

:Parameter: *src*

URL of the svn repo. For example: ``https://svn.example.com/repo/``.

:Parameter: *dst*

Path to export to. For example: ``/tmp/svn_repo``.

mkdir
-----
Create an directory with an remote call.

:Parameter: *folder*

Full URL for the dir to be created. For example:
``https://svn.example.com/repo/dir``

:Parameter: *message*

Commit message.

delete
------
Deletes an file or directory with an remote call.

:Parameter: *target*

Full URL for the dir to be created. For example:
``https://svn.example.com/repo/file``

:Parameter: *message*

Commit message.

create_file
-----------
Create an file path with the given content.

:Parameter: *path*

Full URL for the dir to be created. For example:
``https://svn.example.com/repo/file``

:Parameter: *content*

Content for the file as string.

:Parameter: *message*

Commit message.

checkout
--------
Checkout the given source to the given local destination.

:Parameter: *source*

URL of the svn repo. For example: ``https://svn.example.com/repo/``.

:Parameter: *destination*

Path to export to. For example: ``/tmp/svn_repo``.

checkin
-------
Checkin the given source to the given remote destination.

:Parameter: *source*

Path of the local repository which should to be checked in. For example:
``/tmp/svn_repo``.

:Parameter: *message*

Message for this commit.

add
---
Add the given source to subversion control.

:Parameter: *source*

Path of the local ressource which is to be added. For example:
``/tmp/svn_repo/new_file``.

find
----
Find all files which have the given pattern in the given depth. And return the
results as a list.

:Parameter: *source*

URL of the point to start the search: ``https://svn.example.com/repo/dir``

:Parameter: *pattern*

Regex for the search: ``r'.*\.conf'``

:Parameter: *depth*

The search depth. Found entries which are located deeper, are ignored.

License
=======
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
