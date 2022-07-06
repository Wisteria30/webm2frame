import os
import os.path as op

from natsort import natsorted

from src.clip_frame import clip_frame


def main():
    video_dir = "data/videos"
    save_dir = "data/frames"

    video_files = natsorted(os.listdir(video_dir))
    for video_file in video_files:
        generated_files = clip_frame(op.join(video_dir, video_file), save_dir)
        print(f"{video_file} generated {len(generated_files)} frames")


if __name__ == "__main__":
    main()
