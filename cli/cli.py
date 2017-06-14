import os
import sys
import click

cmd_folder = os.path.join(os.path.dirname(__file__), 'commands')
cmd_prefix = 'cmd_'


class CLI(click.MultiCommand):
    def list_commands(self, ctx):
        """
        Obtain a list of available commands
        :param ctx: List of sorted commands
        """

        commands = []
        for f in os.listdir(cmd_folder):
            if f.startswith(cmd_prefix) and f.endswith('.py'):
                commands.append(f.replace(cmd_prefix, '').replace('.py', ''))

        commands.sort()
        return commands

    def get_command(self, ctx, name):
        """
        Get a specific command by looking up the module
        :param ctx: Click context
        :param name: Command name
        :return: Module's cli function
        """

        ns = {}
        filename = os.path.join(cmd_folder, cmd_prefix + name + '.py')

        try:
            with open(filename) as f:
                code = compile(f.read(), filename, 'exec')
                eval(code, ns, ns)
        except FileNotFoundError:
            print("Command {0} does not exist. Check help menu again".format(name), file=sys.stderr)
            return None

        return ns['cli']


@click.command(cls=CLI)
def cli():
    """
    Commands to help manage the project
    """
    pass