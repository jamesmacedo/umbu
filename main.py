import asyncio
import json
from umbu.core.engine import Engine
from umbu.appearance.animations import FancyAnimation
from umbu.appearance.styles import FancyStyle

engine = Engine()

with open('debug/transcription.json', 'r') as f:
    data = json.load(f)
    engine.load(data)
    asyncio.run(engine.run({'path': "debug/frames"}, FancyAnimation, FancyStyle))
