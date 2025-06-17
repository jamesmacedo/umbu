import asyncio
from core.engine import Engine
from appearance.animations import StaticAnimation
from appearance.styles import StaticStyle
# from appearance.style import DefaultStyle

CHUNK_SIZE = 3
TEXT_PADDING = 20

engine = Engine()
engine.load('debug/transcription.json')
asyncio.run(engine.run(StaticAnimation, StaticStyle))
