import asyncio
from core.engine import Engine
from appearance.animations import DefaultAnimation
from appearance.styles import DefaultStyle

CHUNK_SIZE = 3
TEXT_PADDING = 20

engine = Engine()
engine.load('debug/transcription.json')
asyncio.run(engine.run(DefaultAnimation, DefaultStyle))
