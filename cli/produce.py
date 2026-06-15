import click
import json
from umbu.core.engine import Engine
from umbu.core.transcriber import Transcriber
from umbu.theme.style import minimal_white 


@click.command()
@click.option('-f', '--file', 'file', required=True, help="File to transcriba em produce")
@click.option('-o', '--output', 'output', help="Name of the output file")
def transcribe(file: str, output: str):
    transcriber = Transcriber()
    transcriber.run(file, output)


@click.command()
@click.option('-f', '--file', required=True, help="File to produce")
def run(file: str):
    with open("output/saida.json") as f:
        engine = Engine()
        engine.load(json.load(f), style=minimal_white).run("debug/frames")
