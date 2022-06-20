"""Todo-app entry point script."""
# todo_app/__main__.py

from todo_app import cli, __app_name__

def main():
    """The main entry point for the CLI."""
    cli.app(prog_name=__app_name__)

if __name__ == '__main__':
    main()