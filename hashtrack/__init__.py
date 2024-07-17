import click

__version__ = "0.0.1"


@click.group()
@click.version_option(__version__)
def cli(): ...


from hashtrack import cmd
