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
import os
import unittest

from hostsresolver import hostsfile_source


class TestParseContent(unittest.TestCase):
    def test_parse_content_with_hostname_and_ip(self):
        hostfile_content = '7.7.7.2 my.host.com'
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'my.host.com': '7.7.7.2'})

    def test_parse_content_with_hostname_and_ip_tab_separated(self):
        hostfile_content = '7.7.7.2\tmy.host.com'
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'my.host.com': '7.7.7.2'})

    def test_parse_content_with_hostname_and_ip_multiple_tab_separated(self):
        hostfile_content = '7.7.7.2\t\t\tmy.host.com'
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'my.host.com': '7.7.7.2'})

    def test_parse_content_with_hostname_and_ip_multiple_spaces_separated(self):
        hostfile_content = '7.7.7.2  my.host.com'
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'my.host.com': '7.7.7.2'})
    def test_parse_content_with_hostname_and_ip_multiple_spaces_and_tab_separated(self):
        hostfile_content = '7.7.7.2  \t \t  my.host.com'
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'my.host.com': '7.7.7.2'})

    def test_parse_content_with_hostname_alias(self):
        hostfile_content = '7.7.7.2 my.host.com www.my.host.com'
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'my.host.com': '7.7.7.2','www.my.host.com': '7.7.7.2'})

    def test_parse_content_with_multiple_entries(self):
        hostfile_content = '''
        7.7.7.2 first.host.com
        7.7.7.3 second.host.com
        '''
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'first.host.com': '7.7.7.2',
             'second.host.com': '7.7.7.3'})

    def test_parse_content_with_commented_lines(self):
        hostfile_content = '''
        # 7.7.7.2 first.host.com
        7.7.7.3 second.host.com
        '''
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'second.host.com': '7.7.7.3'})

    def test_parse_content_with_inline_comment(self):
        hostfile_content = '''
        7.7.7.2 first.host.com # www.first.host.com
        7.7.7.3 second.host.com www.second.host.com
        '''
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'first.host.com': '7.7.7.2', 'second.host.com': '7.7.7.3', 'www.second.host.com': '7.7.7.3'})

    def test_parse_content_ignore_localhost_addresses(self):
        hostfile_content = '''
        7.7.7.2 first.host.com
        7.7.7.3 second.host.com
        127.0.0.1 me.host.com
        127.0.1.1 here.host.com
        '''
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'first.host.com': '7.7.7.2', 'second.host.com': '7.7.7.3'})

    def test_parse_content_ignore_anything_but_ipv4(self):
        hostfile_content = '''
        ::1     ip6-localhost ip6-loopback
        fe00::0 ip6-localnet
        ff00::0 ip6-mcastprefix
        ff02::1 ip6-allnodes
        ff02::2 ip6-allrouters
        7.7.7.2 first.host.com
        7.7.7.3 second.host.com
        '''
        self.assertDictEqual(
            hostsfile_source.parse_content(hostfile_content),
            {'first.host.com': '7.7.7.2', 'second.host.com': '7.7.7.3'})


class TestInstall(unittest.TestCase):
    def setUp(self):
        self.hosts_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hosts')

    def test_install_overrides_socket_gethostbyname(self):
        hostsfile_source.install(host_file=self.hosts_file_path)

        import socket
        self.assertEqual(socket.gethostbyname('first.machine.example.org'), '1.1.1.1')
        self.assertEqual(socket.gethostbyname('second.machine.example.org'), '2.3.4.5')
