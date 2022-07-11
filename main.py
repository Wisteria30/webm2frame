import csv
import os
import os.path as op

from moviepy.editor import VideoFileClip
from natsort import natsorted
from tqdm import tqdm


def read_tsv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = [row for row in reader]
    return rows


def save_frameN(
    video_file_path: str, save_dir: str, frame_info: dict, delta: int, N=10
) -> None:
    with VideoFileClip(video_file_path) as clip:
        fps = clip.fps
        start_frame = int(frame_info["startframe"]) + delta
        end_frame = int(frame_info["endframe"]) - delta
        cum_frame = end_frame - start_frame
        if cum_frame >= N:
            div_Nplus1 = cum_frame / (N + 1)
            frame_N = []
            s = delta
            for i in range(N):
                s += div_Nplus1
                frame_N.append(s / fps)
        else:
            frame_N = [i / fps for i in range(start_frame, end_frame + 1)]
        for i, t in enumerate(frame_N):
            clip.save_frame(op.join(save_dir, f"frame{i}.png"), t=t)


def main() -> None:
    video_origin_dir = "data/V3C2/V3C2.webm.videos.shots"
    msb_dir = "data/V3C2/msb"
    save_origin_dir = "data/V3C2/frames"
    delta = 3

    video_dirs = natsorted(os.listdir(video_origin_dir))
    msb_files = natsorted(os.listdir(msb_dir))
    for video_dir, msb_file in tqdm(zip(video_dirs, msb_files)):
        msb = read_tsv(op.join(msb_dir, msb_file))
        video_paths = natsorted(
            list(
                filter(
                    lambda x: op.splitext(x)[1] == ".webm",
                    os.listdir(op.join(video_origin_dir, video_dir)),
                )
            )
        )
        for i, video_path in enumerate(video_paths):
            save_dir = op.join(save_origin_dir, video_dir, video_path)
            os.makedirs(save_dir, exist_ok=True)
            video_file_path = op.join(video_origin_dir, video_dir, video_path)
            save_frameN(video_file_path, save_dir, msb[i], delta)


if __name__ == "__main__":
    main()
