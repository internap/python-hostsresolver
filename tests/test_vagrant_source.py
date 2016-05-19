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

from hostsresolver import vagrant_source


class TestFindVagrantRoot(unittest.TestCase):
    def setUp(self):
        self.origin_vagrant_dotfile_path = vagrant_source.VAGRANT_DOTFILE_PATH
        self.origin_vagrant_vagrantfile = vagrant_source.VAGRANT_VAGRANTFILE
        self.origin_vagrant_cwd = vagrant_source.VAGRANT_CWD
        self.addCleanup(self.cleanupVagrantVariables)

        self.valid_vagrant_root = _resource_path('vagrant_project')
        self.empty_vagrant_root = _resource_path('empty_vagrant_project')
        self.custom_vagrant_root = _resource_path('custom_vagrant_project')

    def cleanupVagrantVariables(self):
        vagrant_source.VAGRANT_DOTFILE_PATH = self.origin_vagrant_dotfile_path
        vagrant_source.VAGRANT_VAGRANTFILE = self.origin_vagrant_vagrantfile
        vagrant_source.VAGRANT_CWD = self.origin_vagrant_cwd

    def test_default_values(self):
        self.assertEqual(vagrant_source.VAGRANT_DOTFILE_PATH, '.vagrant')
        self.assertEqual(vagrant_source.VAGRANT_VAGRANTFILE, 'Vagrantfile')
        self.assertEqual(vagrant_source.VAGRANT_CWD, os.getcwd())

    def test_on_a_sub_folder_of_a_valid_vagrant_root_path(self):
        vagrant_root = self.valid_vagrant_root

        self.assertEqual(
            vagrant_source.lookup_vagrant_root(vagrant_root + '/some/sub/folder'),
            vagrant_root)

    def test_on_a_sub_folder_of_a_valid_vagrant_root_path_using_vagrant_cwd(self):
        vagrant_root = self.valid_vagrant_root

        vagrant_source.VAGRANT_CWD = vagrant_root + '/some/sub/folder'

        self.assertEqual(
            vagrant_source.lookup_vagrant_root(),
            vagrant_root)

    def test_on_a_sub_folder_of_a_custom_vagrant_root_path(self):
        vagrant_source.VAGRANT_DOTFILE_PATH = '.custom_vagrant_internal_data'
        vagrant_source.VAGRANT_VAGRANTFILE = 'custom_vagrantfile'

        valid_vagrant_root = self.custom_vagrant_root

        self.assertEqual(
            vagrant_source.lookup_vagrant_root(valid_vagrant_root + '/some/sub/folder'),
            valid_vagrant_root)


class TestListMachines(unittest.TestCase):
    def setUp(self):
        self.valid_vagrant_root = _resource_path('vagrant_project')
        self.empty_vagrant_root = _resource_path('empty_vagrant_project')

    def test_on_a_valid_vagrant_root_path(self):
        self.assertSetEqual(
            set(vagrant_source.list_machines(vagrant_root=self.valid_vagrant_root)),
            {'first.machine.example.org', 'second.machine.example.org'})

    def test_on_an_invalid_vagrant_root_path(self):
        self.assertListEqual(
            vagrant_source.list_machines(vagrant_root=self.empty_vagrant_root),
            [])

    def test_on_a_sub_folder_of_a_valid_vagrant_root_path(self):
        self.assertSetEqual(
            set(vagrant_source.list_machines(vagrant_root=self.valid_vagrant_root + '/some/sub/folder')),
            {'first.machine.example.org', 'second.machine.example.org'})


class TestKnownHosts(unittest.TestCase):
    def setUp(self):
        self.valid_vagrant_root = _resource_path('vagrant_project')
        self.vagrant_instance = mock.Mock()
        patcher = mock.patch('hostsresolver.vagrant_source.Vagrant')
        patcher.start().return_value = self.vagrant_instance
        self.addCleanup(patcher.stop)

    def test_on_a_valid_vagrant_root_path(self):
        known_hosts = {'first.machine.example.org': '1.1.1.1', 'second.machine.example.org': '2.3.4.5'}
        self.vagrant_instance.hostname.side_effect = known_hosts.get

        self.assertDictEqual(
            vagrant_source.known_hosts(vagrant_root=self.valid_vagrant_root),
            known_hosts)


class TestInstall(unittest.TestCase):
    def setUp(self):
        self.valid_vagrant_root = _resource_path('vagrant_project')
        self.vagrant_instance = mock.Mock()
        patcher = mock.patch('hostsresolver.vagrant_source.Vagrant')
        patcher.start().return_value = self.vagrant_instance
        self.addCleanup(patcher.stop)

    def test_install_overrides_socket_gethostbyname(self):
        known_hosts = {'first.machine.example.org': '1.1.1.1', 'second.machine.example.org': '2.3.4.5'}
        self.vagrant_instance.hostname.side_effect = known_hosts.get

        vagrant_source.install(vagrant_root=self.valid_vagrant_root)

        import socket
        self.assertEqual(socket.gethostbyname('first.machine.example.org'), '1.1.1.1')
        self.assertEqual(socket.gethostbyname('second.machine.example.org'), '2.3.4.5')


def _resource_path(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
