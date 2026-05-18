import os
import math
import shutil
import ffmpeg

import multiprocessing as mp
from umbu.components.base import Component
import umbu.constants as constants

from loguru import logger

from umbu.models.transcription import Transcription
from umbu.models.layout import Word

from umbu.components import Root, Row, Text

from billiard.pool import Pool

from typing import List, Any, Dict

from umbu.models.layout import Word
from umbu.render.cairo.render import CairoRenderer


class Engine:
    _transcription: List[Transcription] = []
    total_frames: int = 0

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

        # ex.: 16 gera [payment, mortgage] [program]
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
    def chunks(self) -> List[List[Transcription]]:
        return self._chunks

    @chunks.setter
    def chunks(self, c) -> List[List[Transcription]]:
        self._chunks = c

    def load(self, transcription: List[Dict]):

        max_longs_per_chunk = 3
        long_len = 6
        max_chars_per_chunk = 16

        self.total_frames = math.ceil(
            transcription[-1]['end'] - transcription[0]['start'])*constants.FPS

        def create_chunk(arr: List[Any], size: int) -> List[List[Word]]:
            chunks: List[List[Word]] = []
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
                chunks.append(raw_chunk)
                i = end

            return chunks
        self._transcription = [Transcription(**d) for d in transcription]
        self.chunks = create_chunk(self._transcription, self.chunk_size)
        return self

    def render_segment(self, component, outfile):

        proc = (
            ffmpeg
            .input('pipe:',
                   format='rawvideo',
                   pix_fmt='bgra',
                   s=f'{constants.WIDTH}x{constants.HEIGHT}',
                   r=constants.FPS)
            .output(outfile,
                    # TODO: check the differences between each of these codecs and pix format
                    vcodec='qtrle',  # qtrle
                    pix_fmt='argb',  # argb
                    movflags='+faststart')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

        # for i in range(start_f, end_f + 1):
        #     frame_bytes = renderer.render(states[i - start_f])
        #     proc.stdin.write(frame_bytes)

        proc.stdin.close()
        proc.wait()

    def test(self, component: Component):
        renderer = CairoRenderer()
        renderer.render(component)

    def run(self, path: str):

        # if os.path.isdir(path) and not os.path.isfile(path):
        #     if os.listdir(path):
        #         shutil.rmtree(path)

        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)

        scene = Root(
            # id="scene",
            children=[
                Row(
                    children=[
                        Text(content=item.word) for item in chunk
                    ]
                ) for chunk in self.chunks[:1]
            ]
        )

        # for chunk in self.chunks:
        #     row = Row()
        #     row2 = Row()
        #     for item in chunk:
        #         text = Text(content=item.word)
        #         row.add_children()
        #     #
        #     # row2.children.append(row)
        #     # row2.children.append(row)
        #     scene.set_child(row)
        #     break

        self.test(scene)

        return

        # TODO: Pass the variable below through the method
        SEG = 500
        segments = [(i, min(i+SEG-1, self.total_frames-1))
                    for i in range(0, self.total_frames, SEG)]

        maxw = min(4, mp.cpu_count())
        # maxw = 4
        with Pool(processes=maxw) as pool:
            results = []
            for seg_id, (start, end) in enumerate(segments):

                args = (
                    self.render_segment,
                    scene,
                    os.path.join(path, f"seg_{seg_id:03d}.mov"))

                res = pool.apply_async(func=args[0], args=args[1:])
                results.append(res)

            for f in results:
                f.get()

        segment_files = [f"seg_{i:03d}.mov" for i in range(len(segments))]
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
