import subprocess


class FFMPEGRepository:
    location_prefix = './tmp'

    def encode(self, scale: str, file_path: str, output_file_path: str) -> str:
        resp = subprocess.run(['ffmpeg', '-y',
                               '-i', file_path,
                               '-vf', f'scale={scale}:-1',
                               '-c:v', 'libx264',
                               '-crf', '18',
                               '-preset', 'slow',
                               '-c:a', 'aac',
                               '-b:a', '128k',
                               output_file_path],
                              capture_output=True, text=True)
        return resp.stderr
