import json
import asyncio
from umbu.core.engine import Engine
from umbu.appearance.animations import MinimalistAnimation
from umbu.appearance.styles import MinimalistStyle

engine = Engine()

with open('debug/transcription.json', 'r') as f:
    data = json.load(f)
    engine.load(data).run("debug/frames", MinimalistAnimation, MinimalistStyle)
