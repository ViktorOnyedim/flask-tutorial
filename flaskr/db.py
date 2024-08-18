import sqlite3
import click
from flask import current_app, g

def get_db():
    """Returns a database connection"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """
        Initializes the database by executing the SQL commands 
        in the 'schema.sql' file. This sets up the necessary tables 
        and schema required for the application to function.
    """

    # get a database connection
    db = get_db()

    # Open and read the schema.sql file, then execute the SQL commands
    with current_app.open_resource('schema.sql') as f: 
        # execute SQL script
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """
        Command-line interface (CLI) command to initialize the database. 
        It calls the `init_db` function to clear existing data and create 
        new tables as defined in 'schema.sql'. Prints a confirmation 
        message once the database has been initialized.
    """

    # Initialize the database
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # Register a teardown function to close the database connection
    app.teardown_appcontext(close_db)
    # Add the 'init-db' CLI command for database initialization
    app.cli.add_command(init_db_command)

