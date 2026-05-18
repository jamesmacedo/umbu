import os
import json
from loguru import logger

from faster_whisper import WhisperModel
from typing import Dict


class Transcriber:

    transcription: list[Dict] = []
    
    def __init__(self):
        self.model = WhisperModel("small", device="cpu", compute_type="int8")

    def run(self, file: str, output: str|None = None):
        segments, _ = self.model.transcribe(file, beam_size=5, word_timestamps=True)

        for segment in segments:
            for word in segment.words:
                self.transcription.append({'content':word.word, 'start':word.start, 'end':word.end})
        
        if output is not None: 
            if not os.path.exists("output"):
                os.mkdir("output")

            with open(f'output/{output}.json', 'w') as f:
                f.write(json.dumps(self.transcription))

        logger.debug("Video transcribed with success!")        
