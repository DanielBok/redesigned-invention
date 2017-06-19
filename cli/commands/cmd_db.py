import click
import numpy.random as rng
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy_utils.types import Choice

from Dashboard.app import create_app
from Dashboard.blueprints.api.models import Tasks, Drivers
from Dashboard.blueprints.user.models import User
from Dashboard.extensions import db
from utils.datetime import now
from utils.extra import ProgressEnumerate
from utils.setup import insert_data

app = create_app()
db.app = app


@click.group()
def cli():
    """
    Group with all database operations
    """
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


@click.command()
def clear_before_now():
    """
    Set all tasks whose flight time <= now as done"
    """
    print("Setting all tasks whose flight time <= now as done")
    tasks = (Tasks.query
             .filter((Tasks.flight_time <= now()) &
                     (Tasks.status != Choice('ready', 'Ready')))
             .all())
    print("Total tasks: ", len(tasks))

    drivers = Drivers.get_all_drivers_names()
    for task in ProgressEnumerate(tasks):
        if task.driver is None:
            task.driver = rng.choice(drivers)
        if task.task_start_time is None:
            task.task_start_time = now()
        task.completed_time = now()
        task.status = Choice('done', 'Done')
        task.task_time_taken = -1
        db.session.add(task)

    db.session.commit()


@click.command()
def clear_after_now():
    """
    Set some tasks as undone. Read code
    """
    print("Setting all tasks whose ready_time <= now as undone")
    tasks = (Tasks.query
             .filter(
        (
            (Tasks.ready_time >= now()) &
            (Tasks.status != Choice('ready', 'Ready'))
        ) |
        (
            (Tasks.flight_time >= now()) &
            (Tasks.ready_time <= now())
        )
        )
             .all())
    print("Total tasks: ", len(tasks))

    for task in ProgressEnumerate(tasks):
        task.status = Choice('ready', 'Ready')
        task.driver = None
        task.task_start_time = None
        db.session.add(task)
    db.session.commit()


@click.command()
@click.pass_context
def clear(ctx):
    """
    Runs clear_before_now() and then clear_after_now()
    """
    ctx.invoke(clear_before_now)
    ctx.invoke(clear_after_now)


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
cli.add_command(clear_before_now)
cli.add_command(clear_after_now)
cli.add_command(clear)
