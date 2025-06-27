import os
import ffmpeg


class Video:

    def sequence(path: str):
        output_video = os.path.join(path, 'captions.mov')
        (
            ffmpeg
            # -framerate 60 -pattern_type glob -i "{path}/*.png"
            .input(os.path.join(path, '*.png'),
                   framerate=60,
                   pattern_type='glob')

            # -c:v prores_ks  -profile:v 4  -pix_fmt yuva444p10le
            .output(output_video,
                    vcodec='prores_ks',
                    pix_fmt='yuva444p10le',
                    **{'profile:v': '4'})      # opções com ":" vão num dict

            .overwrite_output()               # -y
            .run()
        )
        return output_video
