import logging
import click
import json

@click.command()
@click.option("--in", "-i", "in_file", required=True,
              help="Path to geojson file to be processed.", )
@click.option("--id_label", "-l", default='id', help="label for id")
@click.option("--id_start", "-s", default=1, help="first id")
@click.option("--zeros", "-z", default=0,
              help="adds zeros at the beginning of the id")
def process(in_file, id_label, id_start, zeros):
    """
    Add an id in the <properties> in a geojson file
    """
    with open(in_file, 'r') as json_file:
        try:
            json_data = json.load(json_file)

            for i, geo in enumerate(json_data['features'], start=id_start):
                if zeros == 0:
                    geo['properties'][id_label] = i
                else:
                    geo['properties'][id_label] = str(i).zfill(zeros)
        except Exception as e:
            logging.error(e.__str__())
        else:
            print(json_data)


if __name__ == '__main__':
    process()
