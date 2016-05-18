# Copyright 2016 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import os
import unittest

from hostsresolver import vagrant_hostmanager_source


class TestKnownHosts(unittest.TestCase):
    def setUp(self):
        self.valid_vagrant_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vagrant_project')
        self.vagrant_instance = mock.Mock()
        patcher = mock.patch('hostsresolver.vagrant_hostmanager_source.Vagrant')
        patcher.start().return_value = self.vagrant_instance
        self.addCleanup(patcher.stop)

    def test_on_a_valid_vagrant_root_path(self):
        known_hosts = {'first.machine.example.org': '1.1.1.1', 'second.machine.example.org': '2.3.4.5'}
        self.vagrant_instance._run_vagrant_command.return_value = '''
        1.1.1.1 first.machine.example.org
        2.3.4.5 second.machine.example.org
        '''

        self.assertDictEqual(
            vagrant_hostmanager_source.known_hosts(
                vagrant_root=self.valid_vagrant_root),
            known_hosts)

        self.vagrant_instance._run_vagrant_command.assert_called_with(
            ('ssh', 'second.machine.example.org', '-c', 'cat /etc/hosts'))

    def test_on_a_valid_vagrant_root_path_with_specific_host(self):
        known_hosts = {'first.machine.example.org': '1.1.1.1', 'second.machine.example.org': '2.3.4.5'}
        self.vagrant_instance._run_vagrant_command.return_value = '''
        1.1.1.1 first.machine.example.org
        2.3.4.5 second.machine.example.org
        '''

        self.assertDictEqual(
            vagrant_hostmanager_source.known_hosts(
                vagrant_root=self.valid_vagrant_root,
                name='first.machine.example.org'),
            known_hosts)

        self.vagrant_instance._run_vagrant_command.assert_called_with(
            ('ssh', 'first.machine.example.org', '-c', 'cat /etc/hosts'))


class TestInstall(unittest.TestCase):
    def setUp(self):
        self.valid_vagrant_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vagrant_project')
        self.vagrant_instance = mock.Mock()
        patcher = mock.patch('hostsresolver.vagrant_hostmanager_source.Vagrant')
        patcher.start().return_value = self.vagrant_instance
        self.addCleanup(patcher.stop)

    def test_install_overrides_socket_gethostbyname(self):
        self.vagrant_instance._run_vagrant_command.return_value = '''
        1.1.1.1 first.machine.example.org
        2.3.4.5 second.machine.example.org
        '''

        vagrant_hostmanager_source.install(vagrant_root=self.valid_vagrant_root)

        import socket
        self.assertEqual(socket.gethostbyname('first.machine.example.org'), '1.1.1.1')
        self.assertEqual(socket.gethostbyname('second.machine.example.org'), '2.3.4.5')
