import json
from umbu.core.engine import Engine
from umbu.appearance.animations import ModernAnimation, ClassicAnimation
from umbu.appearance.styles import ModernStyle, ClassicStyle

engine = Engine()

with open('debug/transcription.json', 'r') as f:
    data = json.load(f)
    engine.load(data).run("debug/frames", ClassicAnimation, ClassicStyle)
