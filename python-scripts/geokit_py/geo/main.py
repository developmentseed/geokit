import click
from .generateid import generateid


@click.group(chain=True)
def cli():
    click.echo(click.style("========= GEO =============", fg="green"))
    pass


@cli.command("generate_id")
@click.option(
    "--in",
    "-i",
    "in_file",
    required=True,
    help="Path to geojson file to be processed.",
)
@click.option("--id_label", "-l", default="id", help="key for id")
@click.option("--id_start", "-s", default=1, help="value to start id")
@click.option("--zeros", "-z", default=0, help="adds zeros at the beginning of the id")
@click.option("--variation", "-v", default="NUMBER", type=click.Choice(["NUMBER", "UUID"], case_sensitive=False),
              help="type of id (number or uuid)")
@click.option("--output_file", "-o", required=True, type=str, help="Path to geojson output file")
def process(in_file, id_label, id_start, zeros, variation, output_file):
    generateid(in_file, id_label, id_start, zeros, variation, output_file)


if __name__ == "__main__":
    cli()
