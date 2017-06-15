import argparse
import os
import subprocess
from os import getenv

import cherrypy

from Dashboard.app import create_app
from utils.setup import seed, local_db_exists


def make_parser():
    p = argparse.ArgumentParser()

    p.add_argument('-p', '--production',
                   action='store_true',
                   help='Run in production. [Default: False, development mode]')

    p.add_argument('-b', '--build',
                   help='Build commands for Dashboard App',
                   action='store_true')

    return p


app = create_app()

if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()

    if args.build:
        subprocess.call('pip install --editable .', shell=True)
        exit(0)

    if args.production:

        port = int(getenv('PORT', 80))
        static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Dashboard', 'static'))

        cherrypy.tree.graft(app, '/')
        cherrypy.config.update({
            "server.socket_host": "0.0.0.0",
            "server.socket_port": port,
            "tools.staticdir.on": True,
            "tools.staticdir.dir": static_dir,
            "engine.autoreload.on": True
        })

        try:
            cherrypy.engine.start()
            cherrypy.engine.block()
        except KeyboardInterrupt:
            cherrypy.engine.stop()

    else:
        print("%s: Running app in local environment. Development Mode." % __file__)

        if not local_db_exists():
            seed(app)

        app.run(host="0.0.0.0", port=5000)
