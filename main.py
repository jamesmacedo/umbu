import asyncio
from core.engine import Engine
from appearance.animations import DefaultAnimation
# from appearance.style import DefaultStyle

CHUNK_SIZE = 3
TEXT_PADDING = 20

engine = Engine()
engine.load('transcription.json')
asyncio.run(engine.run(DefaultAnimation))
