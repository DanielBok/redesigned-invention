import subprocess

import click

@click.command()
@click.argument('path', default='Dashboard')
def cli(path):
    """
    Runs the test script with coverage
    :param path: Test coverage path
    :return: Subprocess call result
    """
    cmd = "pytest --cov-report term-missing --cov {0}".format(path)
    return subprocess.call(cmd, shell=True)
