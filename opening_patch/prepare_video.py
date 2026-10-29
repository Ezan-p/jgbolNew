"""Optional regeneration of the checked-in compatible opening movie from the original."""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ffmpeg', default='ffmpeg')
    parser.add_argument('--encoder', choices=('libx264', 'h264_videotoolbox'), default='libx264')
    args = parser.parse_args()
    command = [args.ffmpeg, '-hide_banner', '-ignore_editlist', '1',
               '-i', str(ROOT / 'jgbol3.87/res/raw/video.mp4'),
               '-map', '0:v:0', '-map', '0:a:0', '-c:v', args.encoder,
               '-profile:v', 'baseline', '-level:v', '3.0', '-pix_fmt', 'yuv420p',
               '-vf', 'scale=480:270', '-b:v', '550k', '-r', '15', '-g', '30', '-bf', '0']
    if args.encoder == 'h264_videotoolbox':
        command += ['-allow_sw', '1']
    command += ['-c:a', 'aac', '-b:a', '64k', '-ar', '44100', '-af', 'apad',
                '-t', '48.08', '-movflags', '+faststart', '-use_editlist', '0',
                '-y', str(ROOT / 'opening_patch/opening.mp4')]
    subprocess.run(command, check=True)


if __name__ == '__main__':
    main()
