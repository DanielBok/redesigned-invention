import click
from sqlalchemy_utils import database_exists, create_database

from Dashboard.app import create_app
from Dashboard.blueprints.user.models import User
from Dashboard.extensions import db
from utils.setup import insert_data

app = create_app()
db.app = app


@click.group()
def cli():
    pass


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False, help='Run on test db?')
def init(with_testdb):
    """
    Initialize the database
    :param with_testdb: Bool. If true, Create a test database
    :return: None
    """

    print("Dropping and recreating database.", end='\t')
    if with_testdb:
        db_uri = app.config['SQLALCHEMY_DATABASE_URI'].replace('data.db', 'data_test.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

        if not database_exists(db_uri):
            create_database(db_uri)

        db.drop_all()
        db.create_all()
    else:
        db.drop_all()
        db.create_all()

    print("Complete")
    return None


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False, help='Run on test db?')
def seed(with_testdb):
    """
    Seed the database with some data
    :param with_testdb: Bool. If true, apply seed on a test database
    :return: None
    """

    print('Applying seeding operations... ')
    if with_testdb:
        user_seeds = [{
            'role': 'manager',
            'username': 'manager',
            'password': 'test',
            'name': 'Roger Federer'
        }, {
            'role': 'driver',
            'username': 'driver',
            'password': 'test',
            'name': 'John Smith'
        }]

        for u_ in user_seeds:
            u = User.find_by_identity(u_['name'])

            if u is None:
                User(**u_).save()

    else:
        insert_data(db)

    return None


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False, help='Run on test db?')
@click.pass_context
def reset(ctx, with_testdb):
    """
    Init and seed automatically
    :param ctx: application context
    :param with_testdb: create a test database
    :return: None
    """
    ctx.invoke(init, with_testdb=with_testdb)
    ctx.invoke(seed, with_testdb=with_testdb)


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
