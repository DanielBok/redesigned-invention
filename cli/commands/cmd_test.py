import os
import subprocess

import click


@click.command()
@click.option('--cov', is_flag=True)
@click.argument('path', default=os.path.join('Dashboard', 'tests'))
def cli(path, cov):
    """
    Run PyTest. If cov flag is called, test script with coverage
    :param path: path to tests directory
    :param cov: bool, test with coverage
    :return: Subprocess call result
    """
    if cov:
        cmd = "pytest --cov-report term-missing --cov Dashboard"
    else:
        cmd = "pytest {0}".format(path)
    return subprocess.call(cmd, shell=True)
