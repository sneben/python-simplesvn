#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test suite for simplesvn client functionality"""

from mock import patch, call
from unittest2 import TestCase
from simplesvn import SVNClient


class SVNClientTests(TestCase):
    @patch('pysvn.Client', autospec=True)
    def setUp(self, mock_pysvn):
        self.client = SVNClient('testuser', 'testpassword')
        self.mock_pysvn = mock_pysvn

    def test_should_create_directory(self):
        self.client.mkdir('/test', 'Test commit')
        calls = [call.mkdir('/test', 'Test commit', make_parents=False)]
        sub_mock = self.mock_pysvn.return_value
        sub_mock.assert_has_calls(calls)

    def test_should_delete_target(self):
        self.client.delete('/test', 'Test commit')
        calls = [call.remove('/test', force=True)]
        sub_mock = self.mock_pysvn.return_value
        sub_mock.assert_has_calls(calls)

    def test_should_checkout(self):
        self.client.checkout('/source', '/destination')
        calls = [call.checkout('/source', '/destination')]
        sub_mock = self.mock_pysvn.return_value
        sub_mock.assert_has_calls(calls)

    def test_should_checkin(self):
        self.client.checkin('/source', 'Test commit')
        calls = [call.checkin('/source', 'Test commit')]
        sub_mock = self.mock_pysvn.return_value
        sub_mock.assert_has_calls(calls)

    def test_should_add_file(self):
        self.client.add('/source')
        calls = [call.add('/source')]
        sub_mock = self.mock_pysvn.return_value
        sub_mock.assert_has_calls(calls)

    def test_should_get_file_content(self):
        self.client.get_file_content('/path/file')
        calls = [call.cat('/path/file')]
        sub_mock = self.mock_pysvn.return_value
        sub_mock.assert_has_calls(calls)

    def test_should_get_changed_paths(self):
        self.client.get_changed_paths('/svnbase')
        sub_mock = self.mock_pysvn.return_value

    def test_should_create_file(self):
        self.client.create_file('/path/file', 'content', 'Test commit')
        sub_mock = self.mock_pysvn.return_value

    def test_check_callback_ssl_server_trust_prompt(self):
        trust_dict = {'failures': True}
        self.client.callback_ssl_server_trust_prompt(trust_dict)
        self.client.ssl_verify = False
        self.client.callback_ssl_server_trust_prompt(trust_dict)

    def test_check_callback_get_log_message(self):
        self.client.callback_get_log_message()

    def test_check_callback_get_login(self):
        self.client.callback_get_login()

    def test_should_list(self):
        result = self.client.list('https://localhost/svn/repo')

    def test_should_find(self):
        result = self.client.find('https://localhost/svn/repo',
                                  '*.yaml', depth=1)
