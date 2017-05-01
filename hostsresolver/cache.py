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
import sys

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
    def _use_host_cache(self, address):
        try:
            return (gethostbyname(address[0]), address[1])
        except socket.gaierror:
            # The address[0] could be an unknown host to socket.gethostbyname
            # but known to socket.connect, such cases include unix sockets.
            return address

    def connect(self, address):
        return _SocketType.connect(self, self._use_host_cache(address))

    def connect_ex(self, address):
        return _SocketType.connect_ex(self, self._use_host_cache(address))


def update(hosts):
    _hosts_cache.update(hosts)


def clear():
    _hosts_cache.clear()


def install():
    if socket.getaddrinfo is getaddrinfo:
        return  # Already installed

    socket.getaddrinfo = getaddrinfo
    socket.gethostbyname = gethostbyname
    socket.SocketType = SocketType
    socket.create_connection = create_connection
    if sys.version_info > (3,):
        import _socket
        _socket.socket = SocketType
    else:
        socket.socket = SocketType


def uninstall():
    socket.getaddrinfo = _getaddrinfo
    socket.gethostbyname = _gethostbyname
    socket.SocketType = _SocketType
    socket.create_connection = _create_connection
    if sys.version_info > (3,):
        import _socket
        _socket.socket = _SocketType
    else:
        socket.socket = SocketType
