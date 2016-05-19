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

import glob
import os

from vagrant import Vagrant

from hostsresolver.cache import update
from hostsresolver.cache import install as _install_cache

VAGRANT_DOTFILE_PATH = os.environ.get('VAGRANT_DOTFILE_PATH', '.vagrant')
VAGRANT_VAGRANTFILE = os.environ.get('VAGRANT_VAGRANTFILE', 'Vagrantfile')
VAGRANT_CWD = os.environ.get('VAGRANT_CWD', os.getcwd())

vagrant_machines_path = 'machines/*/*/id'.format(**locals())


def lookup_vagrant_root(vagrant_root=None):
    vagrant_root = VAGRANT_CWD if vagrant_root is None else vagrant_root

    path = os.path.abspath(vagrant_root)
    while path != os.path.dirname(path):
        if os.path.exists(os.path.join(path, VAGRANT_VAGRANTFILE)):
            return path
        path = os.path.dirname(path)
    return vagrant_root


def list_machines(vagrant_root=None):
    vagrant_root = lookup_vagrant_root(vagrant_root)
    search_path = os.path.join(vagrant_root, VAGRANT_DOTFILE_PATH, vagrant_machines_path)
    return [path.split(os.path.sep)[-3] for path in glob.glob(search_path)]


def known_hosts(vagrant_root):
    vagrant_root = lookup_vagrant_root(vagrant_root)
    vagrant = Vagrant(vagrant_root)
    return {machine: vagrant.hostname(machine) for machine in list_machines(vagrant_root)}


def install(vagrant_root):
    update(known_hosts(vagrant_root))
    _install_cache()
