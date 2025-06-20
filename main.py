import asyncio
from core.engine import Engine
from appearance.animations import FancyAnimation
from appearance.styles import FancyStyle

engine = Engine()
engine.load('debug/transcription.json')
asyncio.run(engine.run(FancyAnimation, FancyStyle))
