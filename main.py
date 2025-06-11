from core.engine.engine import Engine

CHUNK_SIZE = 3
TEXT_PADDING = 20

engine = Engine()
engine.load('transcription.json')
engine.run()
