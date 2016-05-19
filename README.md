python-hostsresolver
====================
[![Build Status](https://travis-ci.org/internap/python-hostsresolver.svg?branch=master)](https://travis-ci.org/internap/python-hostsresolver)
[![PyPI version](https://badge.fury.io/py/python-hostsresolver.svg)](http://badge.fury.io/py/python-hostsresolver)

Translate ephemeral virtual machines names into IP addresses for python
projects without requiring any modification to the libraries or any
external domain name server. 

Background
----------

When performing integration testing using ephemeral virtual machines,
it is not always convenient to have a real domain name server to
resolve the IP address of each virtual machine, especially if multiple
instances of this test is to be ran simultaneously on the same host.

In most of the cases, it is possible to use directly the IP addresses
of the virtual machines but in some other cases the domain name must
be used.  This is the case for Openstack Keystone where the catalog
contains the URL of the services.

Supported setup
---------------

This project is specifically designed for python projects interacting
with Openstack virtual machines managed by Vagrant.  It is however
possible to make it resolve any name by providing the content of a
hosts file.

Usage
-----

### Standard setup ###

The IP addresses of Vagrant managed virtual machines will be mapped to
the name provided to Vagrant as if it was a hostname.
`vagrant ssh-config` will be used internally to fetch the IP address.

    >>> from hostsresolver import vagrant_source as resolver
    >>> resolver.install('vagrant_project_folder/')


### Using hostmanager plugin ###

It is possible to specify the virtual machine used to download the
hostsfile.  If not provided, the first available virtual machine will
be used.  In this case, we will use `/etc/hosts` downloaded from
`dns.example.org`.

    >>> from hostsresolver import vagrant_hostmanager_source as resolver
    >>> resolver.install('vagrant_project_folder/', 'dns.example.org')

### Using a custom hosts file ###

To simply override some domain name addresses, a custom hosts file may
be loaded.

    >>> from hostsresolver import hostsfile_source as resolver
    >>> resolver.install('my_project_folder/hosts')

Licence
-------

Licensed under the Apache License, Version 2.0

Contributing
------------

Feel free to raise issues and send some pull request, we'll be happy to
look at them!
