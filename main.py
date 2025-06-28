import json
import asyncio
from umbu.core.engine import Engine
from umbu.appearance.animations import FancyAnimation, DefaultAnimation, StaticAnimation
from umbu.appearance.styles import FancyStyle, DefaultStyle, StaticStyle

engine = Engine()

with open('debug/transcription_final.json', 'r') as f:
    data = json.load(f)
    asyncio.run(engine.load(data).run("debug/frames", StaticAnimation, StaticStyle))
