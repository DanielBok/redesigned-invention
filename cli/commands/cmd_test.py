import os
import subprocess

import click


@click.command()
@click.argument('path', default=os.path.join('Dashboard', 'tests'))
def cli(path):
    """
    Run PyTest
    :param path: path to tests directory
    :return: Subprocess call result
    """
    cmd = "pytest {0}".format(path)
    return subprocess.call(cmd, shell=True)
