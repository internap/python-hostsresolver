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

import socket

_getaddrinfo = socket.getaddrinfo
_gethostbyname = socket.gethostbyname
_SocketType = socket.SocketType
_create_connection = socket.create_connection

_hosts_cache = {}


def gethostbyname(host):
    try:
        return _hosts_cache[host]
    except KeyError:
        _hosts_cache[host] = _gethostbyname(host)
    return _hosts_cache[host]


def getaddrinfo(host, port, *args, **kwargs):
    return _getaddrinfo(gethostbyname(host), port, *args, **kwargs)


def create_connection(address, *args, **kwargs):
    host, port = address
    return _create_connection((gethostbyname(host), port), *args, **kwargs)


class SocketType(_SocketType):
    def connect(self, address):
        new_address = (gethostbyname(address[0]), address[1])
        return _SocketType.connect(self, new_address)

    def connect_ex(self, address):
        new_address = (gethostbyname(address[0]), address[1])
        return _SocketType.connect_ex(self, new_address)


def update(hosts):
    _hosts_cache.update(hosts)


def clear():
    _hosts_cache.clear()


def install():
    if socket.getaddrinfo is getaddrinfo:
        return  # Already installed

    socket.getaddrinfo = getaddrinfo
    socket.gethostbyname = gethostbyname
    socket.socket = SocketType
    socket.SocketType = SocketType
    socket.create_connection = create_connection


def uninstall():
    socket.getaddrinfo = _getaddrinfo
    socket.gethostbyname = _gethostbyname
    socket.socket = _SocketType
    socket.SocketType = _SocketType
    socket.create_connection = _create_connection
