import subprocess
from os.path import join
from shutil import copy2

import click
from utils.extra import get_root_file



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

    process = subprocess.Popen("pip freeze".format(file), shell=True, stdout=subprocess.PIPE)
    out, _ = process.communicate()

    with open(get_root_file(file), 'w+') as f:
        text = ""
        for line in out.decode('utf-8').split('\n'):
            line = line.strip()
            if not (line.startswith('-e ') and line.endswith('egg=Dashboard_CLI')):
                text += "{0}\n".format(line)

        f.write(text)
    print("{0} is ready and correct.".format(file))


@click.command()
def push_hook():
    """
    Copies the pre-push hook file to .git/hooks folder.
    pre-push hook runs a test every time before we push to cloud
    :return: None
    """
    source = join(get_root_file(), 'configs', 'pre-push')
    destination = join(get_root_file(), '.git', 'hooks', 'pre-push')
    copy2(source, destination)
    print('Copied pre-push hook over to git hooks folder')


cli.add_command(freeze)
cli.add_command(push_hook)
