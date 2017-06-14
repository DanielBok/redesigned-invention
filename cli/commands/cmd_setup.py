import subprocess
from os.path import join

import click

from configs.settings import ROOT_FOLDER


@click.group()
def cli():
    """
    All operations used to prepare application for production push
    """
    pass


@click.command()
@click.option('--file', default="requirements.txt", help='Name of file to save in [default: requirements.txt]')
def freeze(file):
    """
    Prints the packages into a requirements.txt file without the local editable options
    In other words, there's no local package
    :return: None
    """

    subprocess.call("pip freeze > {0}".format(file))

    with open(join(ROOT_FOLDER, file), 'w+') as f:
        lines = [l.strip() for l in f.readlines() if not (l.startswith('-e ') and l.endswith('egg=Dashboard_CLI'))]
        f.writelines(lines)


cli.add_command(freeze)
