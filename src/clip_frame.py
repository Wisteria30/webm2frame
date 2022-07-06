import os.path as op
from typing import List
from moviepy.editor import VideoFileClip


def clip_frame(video_file_path: str, save_dir: str) -> List[str]:
    with VideoFileClip(video_file_path) as clip:
        created_file = clip.write_images_sequence(op.join(save_dir, 'frame%d.png'))
        return created_file
