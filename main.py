import csv
import os
import os.path as op

import click
from moviepy.editor import VideoFileClip
from natsort import natsorted
from tqdm import tqdm


def read_tsv(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = [row for row in reader]
    return rows


def save_frameN(
    video_file_path: str,
    save_dir: str,
    frame_info: dict,
    delta: int,
    N=10,
    newsize=(640, 360),
) -> None:
    """
    s   @1  @2  @3  @4  @5  @6  @7  @8  @9  @10   e
    | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
    """
    delta = (
        0
        if (int(frame_info["endframe"]) - int(frame_info["startframe"]) - 2 * delta) < N
        else delta
    )

    with VideoFileClip(video_file_path) as clip:
        clip = clip.resize(newsize)
        start_frame = delta
        end_frame = int(frame_info["endframe"]) - int(frame_info["startframe"]) - delta
        cum_frame = end_frame - start_frame
        if cum_frame >= N:
            div_Nplus1 = cum_frame / (N + 1)
            frame_N = []
            for i in range(N):
                start_frame += div_Nplus1
                frame_N.append(start_frame / clip.fps)
        else:
            frame_N = [i / clip.fps for i in range(start_frame, end_frame + 1)]

        for i, t in enumerate(frame_N):
            path = op.join(save_dir, f"{i:04}.png")
            if op.exists(path):
                print(f"{path} already exists")
                continue
            clip.save_frame(path, t=t)


@click.command()
@click.option(
    "--video_origin",
    default="data/V3C2/V3C2.webm.videos.shots",
    help="video origin dir",
)
@click.option("--msb_dir", default="data/V3C2/msb", help="msb dir")
@click.option("--save_origin", default="data/V3C2/frames", help="save origin dir")
@click.option("--delta", default=3, type=int, help="delta frame")
@click.option("--start", default=None, type=int, help="video start")
@click.option("--end", default=None, type=int, help="video end")
def main(video_origin, msb_dir, save_origin, delta, start, end) -> None:
    video_dirs = natsorted(os.listdir(video_origin))
    msb_files = natsorted(os.listdir(msb_dir))
    # slice
    video_dirs = video_dirs[start:end]
    msb_files = msb_files[start:end]
    for video_dir, msb_file in tqdm(zip(video_dirs, msb_files), total=len(video_dirs)):
        msb = read_tsv(op.join(msb_dir, msb_file))
        video_paths = natsorted(
            list(
                filter(
                    lambda x: op.splitext(x)[1] == ".webm",
                    os.listdir(op.join(video_origin, video_dir)),
                )
            )
        )
        for i, video_path in tqdm(enumerate(video_paths), total=len(video_paths)):
            save_dir = op.join(save_origin, video_dir, video_path)
            os.makedirs(save_dir, exist_ok=True)
            video_file_path = op.join(video_origin, video_dir, video_path)
            save_frameN(video_file_path, save_dir, msb[i], delta)
    print("done!")


if __name__ == "__main__":
    main()
