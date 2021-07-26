"""
Script for find school in international schools database and get point if exist.

Author: @developmentseed
"""

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
    Script for find school in international schools database and get point if exist.
    """
    from .code import process

    process(city)


if __name__ == "__main__":
    main()
