from flask.cli import FlaskGroup
from main import create_app, db, migrate

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("db_init")
def db_init():
    """Initialize the database."""
    db.create_all()


if __name__ == '__main__':
    cli()
