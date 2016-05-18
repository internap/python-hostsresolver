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

vagrant_machines_path = '.vagrant/machines/*/*/id'


def list_machines(vagrant_root=None):
    vagrant_root = os.path.abspath(vagrant_root) if vagrant_root is not None else os.getcwd()
    return [path.split(os.path.sep)[-3] for path in glob.glob(os.path.join(vagrant_root, vagrant_machines_path))]


def known_hosts(vagrant_root):
    vagrant_root = os.path.abspath(vagrant_root) if vagrant_root is not None else os.getcwd()
    vagrant = Vagrant(vagrant_root)
    return {machine: vagrant.hostname(machine) for machine in list_machines(vagrant_root)}


def install(vagrant_root):
    update(known_hosts(vagrant_root))
    _install_cache()
