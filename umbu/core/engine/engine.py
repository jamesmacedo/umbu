import os
import math
import shutil
import ffmpeg

import multiprocessing as mp
import umbu.constants as constants

from umbu.core.canva.canva import Canva
from umbu.core.canva.layer import Layer
from umbu.core.models.transcription import Transcription
from umbu.core.models.layout import Word, WordState, Shape
from concurrent.futures import ProcessPoolExecutor

from typing import List, Any, Dict

from umbu.core.models.layout import LayoutState, Word


class Engine:
    _transcription: List[Transcription] = []

    layout: Canva | None = None
    buffer: Layer | None = None

    frame_buffer = []

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

        self._max_chars_per_chunk = 16  # ex.: 16 gera [payment, mortgage] [program]

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

        max_longs_per_chunk = 4
        long_len = 8
        max_chars_per_chunk = 20

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
                item_chunk = [
                    Word(
                        transcription=val,
                        content=val.word.replace('-', ''),
                        state=WordState.UNACTIVATED,
                        shape=Shape()
                    )
                    for val in raw_chunk
                ]
                chunks.append(item_chunk)
                i = end

            return chunks
        self._transcription = [Transcription(**d) for d in transcription]
        self.chunks = create_chunk(self._transcription, self.chunk_size)
        return self

    def _serialize_states(self) -> list:
        serialized = []
        prev_end = 0.0

        previous_chunk = None

        for ci, chunk in enumerate(self.chunks):
            for wi, word in enumerate(chunk):

                prev_chunk = self.chunks[ci - 1] if ci > 0 else None
                next_chunk = self.chunks[ci + 1] if ci < len(self.chunks) - 1 else None

                prev_word = chunk[wi - 1] if wi > 0 else None
                next_word = chunk[wi + 1] if wi < len(chunk) - 1 else None

                n_frames = math.floor(
                    (word.transcription.end - word.transcription.start)
                    * constants.FPS
                )

                if word.transcription.start > prev_end:
                    gap = word.transcription.start - prev_end
                    for _ in range(math.ceil(gap * constants.FPS)):
                        serialized.append(
                            LayoutState(
                                previous_word=None,
                                previous_chunk=None,
                                current_chunk=None,
                                current_word=None,
                                next_word=None,
                                next_chunk=None
                            ))

                for i in range(0, n_frames):
                    serialized.append(
                        LayoutState(
                            previous_word=prev_word,
                            previous_chunk=prev_chunk,

                            current_chunk=chunk,
                            current_word=word.copy(update={'total_frames': n_frames, 'current_frame': i}),

                            next_word=next_word,
                            next_chunk=next_chunk
                        ))

                prev_end = word.transcription.end

        return serialized

    def render_segment(self, start_f, end_f, states, classe, style, outfile):

        canva = Canva(style)

        proc = (
            ffmpeg
            .input('pipe:',
                   format='rawvideo',
                   pix_fmt='bgra',
                   s=f'{constants.WIDTH}x{constants.HEIGHT}',
                   r=constants.FPS)
            .output(outfile,
                    # TODO: check the differences between each of these codecs and pix format
                    vcodec='qtrle', # qtrle
                    pix_fmt='argb', # argb
                    movflags='+faststart')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )

        for i in range(start_f, end_f + 1):
            frame_bytes = classe(canva).draw(states[i - start_f])
            proc.stdin.write(frame_bytes)

        proc.stdin.close()
        proc.wait()

    def debug(self, path: str, classe, style):

        # if os.path.isdir(path) and not os.path.isfile(path):
        #     if os.listdir(path):
        #         shutil.rmtree(path)

        serialized = self._serialize_states()
        canva = Canva(style)

        for i, state in enumerate(serialized):
            classe(canva).draw(state)

        # self.build(classe, style)
        # return Video.sequence(path)

    def run(self, path: str, classe, style):

        # if os.path.isdir(path) and not os.path.isfile(path):
        #     if os.listdir(path):
        #         shutil.rmtree(path)

        if os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)

        states = self._serialize_states()
        total_frames = len(states)

        # TODO: Pass the variable below through the method
        SEG = 500
        segments = [(i, min(i+SEG-1, total_frames-1))
                    for i in range(0, total_frames, SEG)]

        # print(segments)
        # return

        maxw = min(40, mp.cpu_count())
        with ProcessPoolExecutor(max_workers=maxw) as pool:
            futs = []
            for seg_id, (start, end) in enumerate(segments):
                futs.append(
                    pool.submit(
                        self.render_segment,
                        start,
                        end,
                        states[start:end+1],
                        classe,
                        style,
                        os.path.join(path, f"seg_{seg_id:03d}.mov"))
                )
            for f in futs:
                f.result()

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

        print("✅ Video created with sucess:", os.path.join(path, "caption.mov"))
        return os.path.join(path, "caption.mov")
