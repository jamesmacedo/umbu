import asyncio
import json
from umbu.core.engine import Engine
from umbu.appearance.animations import FancyAnimation
from umbu.appearance.styles import FancyStyle

engine = Engine()

with open('debug/transcription.json', 'r') as f:
    data = json.load(f)
    asyncio.run(engine.load(data).run("debug/frames", FancyAnimation, FancyStyle))
