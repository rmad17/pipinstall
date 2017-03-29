#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 rmad17 <souravbasu17@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import click

from sh import mv as sh_mv
from sh import pip as sh_pip
from sh import rm as sh_rm


@click.group()
@click.version_option()
def pipin():
    """
    Entry point for pipin
    """
    pass


@pipin.command()
@click.argument('packagename')
@click.option('--save', is_flag=True, help='pin package to requirements')
@click.option('--save-dev', is_flag=True,
              help='pin package to dev-requirements')
@click.option('--save-test', is_flag=True,
              help='pin package to test-requirements')
@click.argument('filename', required=False)
def install(packagename, save, save_dev, save_test, filename):
    """
    Install the package via pip, pin the package only to requirements file.
    Use option to decide which file the package will be pinned to.
    """
    print('Installing ', packagename)
    print(sh_pip.install(packagename))
    if not filename:
        filename = get_filename(save, save_dev, save_test)
    add_requirements(packagename, filename)


@pipin.command()
@click.argument('packagename')
@click.argument('filename', required=False)
def remove(packagename, filename):
    print(sh_pip.uninstall(packagename, "-y"))
    if not filename:
        filename = get_filename()
    remove_requirements(packagename, filename)


def add_requirements(packagename, filename):
    output = sh_pip.freeze
    packages = output.split('\n')
    for req in packages:
        if not req:
            continue
        if packagename in req:
            with open(filename, 'ab+') as f:
                f.write(req.encode('utf-8'))

    print('Updated', str(filename) + '!')


def remove_requirements(packagename, filename):
    with open(filename, 'rb+') as f0:
        for line in f0.readlines():
            if packagename not in str(line):
                with open(filename + '.tmp', 'wb+') as f1:
                    f1.write(line)
    sh_rm(filename, "-f")
    sh_mv(filename + '.tmp', filename)
    print('Updated', str(filename) + '!')


def get_filename(save=False, save_dev=False, save_test=False):
    if save_dev:
        return 'dev-requirements.txt'
    if save_test:
        return 'test-requirements.txt'
    return 'requirements.txt'


if __name__ == '__main__':
    pipin()
