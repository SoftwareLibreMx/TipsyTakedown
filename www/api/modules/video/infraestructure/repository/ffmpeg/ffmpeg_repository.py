import subprocess


class FFMPEGRepository:
    location_prefix = './tmp'

    def encode(self, scale: str, file_name: str) -> str:
        output_f_name = f'{file_name}_output_{scale}.mp4'
        file_output_name = f'{self.location_prefix}/{output_f_name}'
        resp = subprocess.run(['ffmpeg', '-y',
                               '-i', f'{self.location_prefix}/{file_name}',
                               '-vf', f'scale={scale}:-1',
                               '-c:v', 'libx264',
                               '-crf', '18',
                               '-preset', 'slow',
                               '-c:a', 'aac',
                               '-b:a', '128k',
                               file_output_name], capture_output=True, text=True)

        print(resp.stdout)
        return file_output_name
