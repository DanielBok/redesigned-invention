import os
import subprocess
import click


@click.command()
@click.option('--cov', is_flag=True)
@click.option('--pushing', is_flag=True)
@click.argument('path', default=os.path.join('Dashboard', 'tests'))
def cli(path, cov, pushing):
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

    # out = os.system(cmd)
    # out = subprocess.check_output(cmd.split(), shell=True)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, err = p.communicate()

    with open('test_results.txt', 'w') as f:
        f.write(output.decode('utf-8'))
