# Copyright 2016 Internap.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from vagrant import Vagrant

from hostsresolver.hostsfile_source import parse_content
from hostsresolver.vagrant_source import list_machines, lookup_vagrant_root
from hostsresolver.cache import update
from hostsresolver.cache import install as _install_cache


def known_hosts(vagrant_root, name=None):
    vagrant_root = lookup_vagrant_root(vagrant_root)
    vagrant = Vagrant(vagrant_root)

    machines = list_machines(vagrant_root)
    name = name if name in machines else machines[0]

    return parse_content(vagrant._run_vagrant_command(('ssh', name, '-c', 'cat /etc/hosts')))


def install(vagrant_root=None):
    update(known_hosts(vagrant_root))
    _install_cache()
