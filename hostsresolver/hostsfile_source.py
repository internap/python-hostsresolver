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

from hostsresolver.cache import update
from hostsresolver.cache import install as _install_cache


def parse_content(content):
    hosts = {}
    for line in content.split('\n'):
        items = line.split('#')[0].strip().split()
        if len(items) < 2:
            continue
        address = items[0]
        names = items[1:]
        split_ipv4 = address.split('.')
        if len(split_ipv4) != 4:
            continue
        if split_ipv4[0] == '127':
            continue
        for name in names:
            hosts[name] = address
    return hosts


def known_hosts(hosts_file):
    with open(hosts_file) as file:
        return parse_content(file.read())


def install(host_file):
    update(known_hosts(host_file))
    _install_cache()
