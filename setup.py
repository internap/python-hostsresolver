from distutils.core import setup

setup(
    name='python-hostsresover',
    packages=['hostsresolver'],
    url='https://github.com/internap/python-hostsresover',
    license='Apache License, Version 2.0',
    author='Internap Hosting',
    author_email='opensource@internap.com',
    description=
        'Translate ephemeral virtual machines names into IP addresses for python projects without requiring '
        'any modification to the libraries or any external domain name server.',
    install_requires=[
        'python-vagrant',
    ]
)
