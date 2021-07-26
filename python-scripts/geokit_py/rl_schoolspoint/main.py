import click


@click.command()
@click.option(
    "--city",
    "-c",
    "city",
    required=True,
    help="Name of city.",
)
def main(city):
    """
    Removes the objects with action=delete in a osm file.
    """
    from .code import process

    process(city)


if __name__ == "__main__":
    main()
