import click
from .intersectionbox import intersectionbox
from .smallbox import smallbox


@click.group(chain=True)
def cli():
    click.echo(click.style("========= CVAT =============", fg="green"))
    pass


@cli.command("intersectionbox")
@click.option(
    "--in",
    "-i",
    "in_file",
    required=True,
    help="Path to xml cvt file to be processed.",
)
@click.option(
    "--toleranci",
    "-t",
    default=70.0,
    help="toleranci to filter box area, default 70 (70% area of image, max area is 100%).",
)
def run_intersectionbox(in_file, toleranci):
    """
    validate if tag include in tiles_error
    """
    intersectionbox(in_file, toleranci)


@cli.command("smallbox")
@click.option(
    "--in",
    "-i",
    "in_file",
    required=True,
    help="Path to xml cvt file to be processed.",
)
@click.option(
    "--toleranci",
    "-t",
    default=1.0,
    help="toleranci to filter box area, default 1 (1% area of image).",
)
def run_smallbox(in_file, toleranci):
    """
    Processes the area of cvt file and filter small boxes
    """
    smallbox(in_file, toleranci)


if __name__ == "__main__":
    cli()
