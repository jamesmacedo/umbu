import os
import math
import shutil
import ffmpeg

from umbu.components.base import Component
import umbu.constants as constants

from umbu.models.transcription import Transcription

from umbu.components import Root, Row, Text

from billiard.pool import Pool

from typing import List, Any, Dict

from umbu.render.cairo.render import CairoRenderer
from pydantic import BaseModel
from umbu.theme.style.interface import Style, Animation

class Chunk(BaseModel):
    total_frames: int = 0
    words: list[Transcription] = []

class Size(BaseModel):
    width: int = constants.WIDTH 
    height: int = constants.HEIGHT

class Engine:
    _transcription: List[Transcription] = []
    total_frames: int = 0

    _FPS: int = constants.FPS 
    animation: Animation
    style: Style 
    _size: Size

    def __init__(self):
        self._chunk_size = constants.CHUNK_SIZE

    @property
    def chunk_size(self):
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, value):
        if value < 0:
            raise ValueError("The chunk size should be an positive value")

        self._chunk_size = value

        self._max_chars_per_chunk = 16

    @property
    def max_chars_per_chunk(self) -> int | None:
        return self._max_chars_per_chunk

    @max_chars_per_chunk.setter
    def max_chars_per_chunk(self, value: int | None):
        if value is not None and value <= 0:
            raise ValueError("max_chars_per_chunk deve ser positivo ou None")
        self._max_chars_per_chunk = value

    @property
    def chunks(self) -> List[Chunk]:
        return self._chunks

    @chunks.setter
    def chunks(self, c):
        self._chunks = c

    def size(self, size: str) -> 'Engine':

        if 'x' not in size:
            raise ValueError("Please provide the size using the following pattern: 720x1280") 

        w, h = size.split('x') 
        self._size = Size(width=int(w), height=int(h))
        return self
    
    def fps(self, fps: int) -> 'Engine':
        self._FPS = int(fps) 
        return self

    def load(self, transcription: List[Dict], style: Style):

        self.style = style

        max_longs_per_chunk = 3
        long_len = 6
        max_chars_per_chunk = 16

        self.total_frames = math.ceil(
            transcription[-1]['end'] - transcription[0]['start'])*self._FPS

        def create_chunk(arr: List[Any], size: int) -> List[Chunk]:
            chunks: List[Chunk] = []
            i = 0
            n = len(arr)
            while i < n:
                end = i
                long_count = 0
                total_chars = 0

                while end < n and (end - i) < size:
                    raw = arr[end].word
                    w = raw.replace('-', '')
                    wlen = len(w)

                    if max_chars_per_chunk is not None and (total_chars + wlen) > max_chars_per_chunk:
                        break

                    if wlen >= long_len and long_count >= max_longs_per_chunk:
                        break

                    if wlen >= long_len:
                        long_count += 1
                    total_chars += wlen
                    end += 1

                while end < n and (arr[end].word.endswith('.') or arr[end].word.endswith(',')):
                    end += 1
                raw_chunk = arr[i:end]
                chunks.append(Chunk(words=raw_chunk, total_frames=sum(chunk.total_frames for chunk in raw_chunk)))
                i = end

            return chunks

        self._transcription = [Transcription(**{'total_frames': math.ceil((d['end'] - d['start'])*self._FPS)}|d) for d in transcription]
        self.chunks = create_chunk(self._transcription, self.chunk_size)
        return self

    def render_segment(self, row,outfile: str):

        renderer = CairoRenderer(self._size.width, self._size.height)
        renderer.setup(row)
        proc = (
            ffmpeg
            .input('pipe:',
                   format='rawvideo',
                   pix_fmt='bgra',
                   s=f'{self._size.width}x{self._size.height}',
                   r=self._FPS)
            .output(outfile,
                    # TODO: check the differences between each of these codecs and pix format
                    vcodec='qtrle',  # qtrle
                    pix_fmt='argb',  # argb
                    movflags='+faststart')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

        # for i in range(row.start_frame, row.end_frame + 1):
        for text in row.children: 
            for j in range(text.total_frames + 1):
                proc.stdin.write(renderer.render(row))
                renderer.setup(row)
                text.update(j)
            # row.update(i)

        proc.stdin.close()
        proc.wait()

    def run(self, path: str):

        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)

        t_start_chunk = self.chunks[0].words[0].start if self.chunks[0].words else 0

        scene = Root(
            width=self._size.width,
            height=self._size.height,
            children=[
                Row(
                    total_frames=chunk.total_frames,
                    start_frame=0,
                    end_frame=chunk.total_frames,
                    children=[
                        Text(
                            style=self.style,
                            content=item.word,
                            total_frames=item.total_frames,
                            start_frame=math.ceil((item.start - t_start_chunk) * self._FPS),
                            end_frame=math.ceil((item.end - t_start_chunk) * self._FPS),
                        ) for item in chunk.words
                    ]
                ) for chunk in self.chunks[:3]
            ]
        )

        # TODO: Pass the variable below through the method
        # SEG = 500
        # segments = [(i, min(i+SEG-1, self.total_frames-1))
        #             for i in range(0, self.total_frames, SEG)]

        # SEG = 40 
        # segments = [scene.children[i:i + SEG] for i in range(0, len(scene.children), SEG)]

        # maxw = min(4, mp.cpu_count())
        maxw = 4
        with Pool(processes=maxw) as pool:
            results = []
            for seg_id, row in enumerate(scene.children):
                args = (
                    self.render_segment,
                    row,
                    os.path.join(path, f"seg_{seg_id:03d}.mov"))

                res = pool.apply_async(func=args[0], args=args[1:])
                results.append(res)

            for f in results:
                f.get()

        segment_files = [f"seg_{i:03d}.mov" for i in range(len(scene.children))]
        list_path = os.path.join(path, "segments.txt")

        with open(list_path, "w", encoding="utf8") as f:
            for fname in segment_files:
                f.write(f"file '{fname}'\n")

        (
            ffmpeg
            .input(list_path, format='concat', safe=0)
            .output(os.path.join(path, "caption.mov"),
                    vcodec='copy',
                    )
            .overwrite_output()
            .run()
        )

        print("✅ Video created with sucess:",
              os.path.join(path, "caption.mov"))
        return os.path.join(path, "caption.mov")
