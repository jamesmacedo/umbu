import click
import json
from umbu.core.engine import Engine
from umbu.core.transcriber import Transcriber
from umbu.theme.style import minimal_yellow, minimal_white, scale, bounce


@click.command()
@click.option('-f', '--file', 'file', required=True, help="File to transcriba em produce")
@click.option('-o', '--output', 'output', help="Name of the output file")
def transcribe(file: str, output: str):
    transcriber = Transcriber()
    transcriber.run(file, output)


@click.command()
@click.option('-i', '--input', 'input_file', required=True, help="File to produce")
@click.option('-s', '--size', required=False, help="The target video resolution size e.g. 720x1280")
@click.option('-f', '--fps', required=False, help="The target video FPS") 
def run(input_file: str, size: str, fps: int):
    with open("output/saida.json") as f:
        engine = Engine()

        engine.load(json.load(f), style=scale)

        if(size):
            engine.size(size)

        if(fps):
            engine.fps(fps)

        engine.run("debug/frames")
