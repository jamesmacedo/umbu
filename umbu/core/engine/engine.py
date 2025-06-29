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

    @property
    def chunks(self) -> List[List[Transcription]]:
        return self._chunks

    @chunks.setter
    def chunks(self, c) -> List[List[Transcription]]:
        self._chunks = c

    def load(self, transcription: List[Dict]):
        def create_chunk(arr: List[Any], size: int) -> List[List[Word]]:
            chunks: List[List[Word]] = []
            for i in range(0, len(arr), size):
                raw_chunk = arr[i:i + size]
                item_chunk = [
                    Word(
                        transcription=val,
                        content=val.word,
                        state=WordState.UNACTIVATED,
                        shape=Shape()
                    )
                    for val in raw_chunk
                ]
                chunks.append(item_chunk)
            return chunks

        self._transcription = [Transcription(**d) for d in transcription]
        self.chunks = create_chunk(self._transcription, self.chunk_size)
        return self

    def _serialize_states(self) -> list:
        serialized = []
        prev_end = 0.0

        for chunk in self.chunks:
            for word in chunk:

                # gap = word.transcription.start - prev_end
                # if gap > 0:
                #     silent_frames = math.ceil(gap * constants.FPS)
                #     serialized.extend([{"word": None}] * silent_frames)

                n_frames = math.ceil(
                    (word.transcription.end - word.transcription.start)
                    * constants.FPS
                )

                if word.transcription.start > prev_end:
                    print("has gap")
                    gap = word.transcription.start - prev_end
                    for _ in range(math.ceil(gap * constants.FPS)):
                        serialized.append(
                            LayoutState(
                                current_chunk=None,
                                current_word=None
                            ))

                for i in range(0, n_frames):
                    serialized.append(
                        LayoutState(
                            current_chunk=chunk,
                            current_word=word.copy(update={'total_frames': n_frames, 'current_frame': i})
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

    async def debug(self, path: str, classe, style):

        # if os.path.isdir(path) and not os.path.isfile(path):
        #     if os.listdir(path):
        #         shutil.rmtree(path)

        serialized = self._serialize_states()
        canva = Canva(style)

        for i, state in enumerate(serialized):
            classe(canva).draw(state)

        # self.build(classe, style)
        # return Video.sequence(path)

    async def run(self, path: str, classe, style):

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
