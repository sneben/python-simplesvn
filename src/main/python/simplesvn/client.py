#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pysvn
import shutil
import tempfile


class RemoteFileNotFoundError(Exception):
    """Exception class for throwing RemoteFileNotFoundError exceptions"""
    pass


class SVNClient(object):
    """Class subversion usage with specialized calls"""

    def __init__(self, user, password, ssl_verify=True):
        self._client = pysvn.Client()
        self._user = user
        self._password = password
        self._client.callback_ssl_server_trust_prompt = self.callback_ssl_server_trust_prompt
        self._client.callback_get_login = self.callback_get_login
        self._client.callback_get_log_message = self.callback_get_log_message
        self._log_message = None
        self.ssl_verify = ssl_verify

    def callback_get_log_message(self):
        """Some pysvn function take the log message over an callback function"""
        return True, self._log_message

    def callback_ssl_server_trust_prompt(self, trust_dict):
        """Callback handler when a login is needed"""
        if self.ssl_verify:
            return True, 0, True
        else:
            return True, trust_dict['failures'], True

    def callback_get_login(self, *args):
        """Callback handler if we need to accept a certificate"""
        return True, self._user, self._password, False

    def list(self, source, recursive=False):
        """Make an ls on the given svn path"""
        if recursive:
            depth = pysvn.depth.infinity
        else:
            depth = pysvn.depth.immediates
        entries = []
        for entry in self._client.list(source, depth=depth):
            if not source.endswith(entry[0].repos_path):
                entries.append(entry[0].repos_path.replace('//', '/'))
        return entries

    def get_changed_paths(self, source, start=1):
        """Build a summary dict of all changed files under the given source"""
        path_list = []
        log = self._client.log(source, discover_changed_paths=True, limit=1)
        for entry in log:
            paths = entry.get('changed_paths')
            for path in paths:
                # Ignore deleted folders/files, but always add entries
                # with path count greater than the given start value
                if not (path.get('action') == 'D' and
                   len(filter(None, path.get('path').split('/'))) <= start):
                    path_list.append(path.get('path'))
        return path_list

    def get_file_content(self, source=None):
        """Read out the content of the given file directly from subversion"""
        try:
            return self._client.cat(source)
        except pysvn.ClientError as error:
            if 'path not found' in error:
                raise RemoteFileNotFoundError(error)

    def exists(self, source):
        """Check if the given svn ressource exists"""
        try:
            self._client.list(source)
        except pysvn.ClientError as error:
            if 'non-existent' in str(error):
                return False
            else:
                raise
        return True

    def export(self, src, dst):
        """Checkout files or directories and return the revision number"""
        revision = self._client.export(src, dst, force=True)
        start = pysvn.Revision(pysvn.opt_revision_kind.number, revision.number)
        end = pysvn.Revision(pysvn.opt_revision_kind.number, revision.number)
        log = self._client.log(src, revision_start=start, revision_end=end)
        message = ''
        if log:
            message = log[0].message
        return [revision.number, message]

    def mkdir(self, folder, message):
        """Create an directory with an remote call"""
        self._client.mkdir(folder, message, make_parents=False)

    def delete(self, target, message):
        """Deletes an file or directory with an remote call"""
        self._log_message = message
        self._client.remove(target, force=True)

    def create_file(self, path, content, message):
        """Create an fipathle with the given content"""
        workdir = tempfile.mkdtemp(prefix="simplesvn-tmp-")
        folder_url = '/'.join(path.split('/')[0:-1])
        self._client.checkout(folder_url, workdir)
        file_path = workdir + '/' + '/' + str(path.split('/')[-1])
        with open(file_path, 'w') as new_file:
            new_file.write(str(content))
        self._client.add(file_path)
        self._client.checkin(file_path, message)
        shutil.rmtree(workdir)

    def checkout(self, source, destination):
        """Checkout the given source to the given local destination"""
        self._client.checkout(source, destination)

    def checkin(self, source, message):
        """Checkin the given source to the given remote destination"""
        self._client.checkin(source, message)

    def add(self, source):
        """Add the given source to subversion control"""
        self._client.add(source)

    def find(self, source, pattern, depth=1):
        """Find all files which have the given pattern in the given depth"""
        result_list = []
        for entry in self._client.list(source, depth=pysvn.depth.infinity):
            entry = entry[0].repos_path.replace('//', '/')
            # +1 of depth, because split produces a empty leading '' here
            if len(entry.split('/')) <= depth + 1:
                if re.match(pattern, entry.split('/')[-1]):
                    result_list.append(entry)
        return result_list
