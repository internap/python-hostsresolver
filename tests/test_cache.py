# Copyright 2016 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributedvagrant_instance under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket
import unittest

from hostsresolver import cache


class TestGetHostByName(unittest.TestCase):
    def setUp(self):
        cache.uninstall()

    def test_initial_state(self):
        self.assertRaises(socket.gaierror, socket.gethostbyname, 'first.machine.example.org')
        self.assertEqual(socket.gethostbyname('google-public-dns-a.google.com'), '8.8.8.8')

    def test_install_overrides(self):
        cache.clear()
        cache.install()
        self.assertRaises(socket.gaierror, socket.gethostbyname, 'first.machine.example.org')
        self.assertEqual(socket.gethostbyname('google-public-dns-a.google.com'), '8.8.8.8')

        cache.update({'first.machine.example.org': '1.1.1.1'})
        self.assertEqual(socket.gethostbyname('first.machine.example.org'), '1.1.1.1')
        self.assertEqual(socket.gethostbyname('google-public-dns-a.google.com'), '8.8.8.8')

    def test_uninstall_returns_original_state(self):
        cache.install()
        cache.update({'first.machine.example.org': '1.1.1.1'})
        cache.uninstall()

        self.assertRaises(socket.gaierror, socket.gethostbyname, 'first.machine.example.org')
        self.assertEqual(socket.gethostbyname('google-public-dns-a.google.com'), '8.8.8.8')


class TestGetAddrInfo(unittest.TestCase):
    def setUp(self):
        cache.uninstall()

    def test_initial_state(self):
        self.assertRaises(socket.gaierror, socket.getaddrinfo, 'first.machine.example.org', 22)

        # Here we only get IPv4 & IPv6 data as we DON'T use our name resolution
        self.assertListEqual(
            socket.getaddrinfo('google-public-dns-a.google.com', 53),
            [(2, 1, 6, '', ('8.8.8.8', 53)),
             (2, 2, 17, '', ('8.8.8.8', 53)),
             (2, 3, 0, '', ('8.8.8.8', 53)),
             (10, 1, 6, '', ('2001:4860:4860::8888', 53, 0, 0)),
             (10, 2, 17, '', ('2001:4860:4860::8888', 53, 0, 0)),
             (10, 3, 0, '', ('2001:4860:4860::8888', 53, 0, 0))])

    def test_install_overrides(self):
        cache.clear()
        cache.install()
        self.assertRaises(socket.gaierror, socket.getaddrinfo, 'first.machine.example.org', 22)
        # Here we only get IPv4 data as we use our name resolution
        self.assertListEqual(
            socket.getaddrinfo('google-public-dns-a.google.com', 53),
            [(2, 1, 6, '', ('8.8.8.8', 53)),
             (2, 2, 17, '', ('8.8.8.8', 53)),
             (2, 3, 0, '', ('8.8.8.8', 53))])

        cache.update({'first.machine.example.org': '1.1.1.1'})
        self.assertListEqual(
            socket.getaddrinfo('first.machine.example.org', 80),
            [(2, 1, 6, '', ('1.1.1.1', 80)),
             (2, 2, 17, '', ('1.1.1.1', 80)),
             (2, 3, 0, '', ('1.1.1.1', 80))])

        # Here we only get IPv4 data as we use our name resolution
        self.assertListEqual(
            socket.getaddrinfo('google-public-dns-a.google.com', 53),
            [(2, 1, 6, '', ('8.8.8.8', 53)),
             (2, 2, 17, '', ('8.8.8.8', 53)),
             (2, 3, 0, '', ('8.8.8.8', 53))])

    def test_uninstall_returns_original_state(self):
        cache.install()
        cache.update({'first.machine.example.org': '1.1.1.1'})
        cache.uninstall()

        self.assertRaises(socket.gaierror, socket.getaddrinfo, 'first.machine.example.org', 22)

        # Here we only get IPv4 & IPv6 data as we DON'T use our name resolution anymore
        self.assertListEqual(
            socket.getaddrinfo('google-public-dns-a.google.com', 53),
            [(2, 1, 6, '', ('8.8.8.8', 53)),
             (2, 2, 17, '', ('8.8.8.8', 53)),
             (2, 3, 0, '', ('8.8.8.8', 53)),
             (10, 1, 6, '', ('2001:4860:4860::8888', 53, 0, 0)),
             (10, 2, 17, '', ('2001:4860:4860::8888', 53, 0, 0)),
             (10, 3, 0, '', ('2001:4860:4860::8888', 53, 0, 0))])
