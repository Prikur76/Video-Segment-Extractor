import os
import argparse
from multiprocessing import Process
from moviepy import VideoFileClip
from utils.app_logger import get_logger


logger = get_logger(__name__)


def compress_video(
    input_file_path: str, output_file_path: str, fps: float = 0.00, codec: str = "libx264", duration: float = None
) -> None:
    """
    Compresses video to the specified parameters.

    Args:
        input_file_path (str): Path to the input video file.
        output_file_path (str): Path to the output video file.
        fps (float): Target frame rate for the video.
        codec (str): Codec to use for compression.
        duration (float): Duration of the video (in seconds).

    Raises:
        FileNotFoundError: If the input file is not found.
    """
    if not os.path.isfile(input_file_path):
        raise FileNotFoundError(f"Input file not found: {input_file_path}")

    with VideoFileClip(input_file_path) as video:
        if fps > 0.00 and fps != video.fps:
            video = video.with_fps(fps)
        if duration:
            video = video.subclipped(0, duration)  # Specify the start and end time
        video.write_videofile(
            output_file_path,
            codec=codec,
            audio_codec="aac"
        )

    if not os.path.isfile(output_file_path):
        raise FileNotFoundError(f"Compressed file not created: {output_file_path}")


def process_single_video(input_file: str, output_folder: str, fps: float, index: int, total_files: int, codec: str = "libx264", duration: float = None) -> None:
    """Processes a single video file and compresses it."""
    filename = os.path.basename(input_file)
    logger.info(f"Processing file {index}/{total_files}: {filename}")

    with VideoFileClip(input_file) as video:
        video_info = {
            "filename": filename,
            "size_mb": round(os.path.getsize(input_file) / 1024**2, 0),
            "width": video.w,
            "height": video.h,
            "fps": video.fps,
            "total_frames": int(video.duration * video.fps)  # Assuming total frames based on fps and duration
        }

    output_filename = f"video_{index}_{video_info['width']}x{video_info['height']}x{fps}"
    if duration:
        output_filename += f"_{duration}"
    output_filename += ".mp4"
    output_file = os.path.join(output_folder, output_filename)

    compress_video(input_file, output_file, fps, codec, duration)
    logger.info(f"Finished processing {output_filename}.")


def process_video_files(input_dir: str, output_dir: str, fps: float = 0.0, codec: str = "libx264", duration: float = None) -> None:
    """Compress all video files in the specified input directory."""
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    os.makedirs(output_dir, exist_ok=True)
    video_files = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]
    
    processes = []
    for idx, video_file in enumerate(video_files):
        process = Process(
            target=process_single_video, 
            args=(os.path.join(input_dir, video_file), output_dir, fps, idx + 1, len(video_files), codec, duration)
        )
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


def main():
    parser = argparse.ArgumentParser(description="Compress video files in a specified directory.")
    parser.add_argument("input_dir", help="Directory containing input video files.")
    parser.add_argument("output_dir", help="Directory to save compressed video files.")
    parser.add_argument("--codec", type=str, default="libx264", help="Codec to use for video compression.")
    parser.add_argument("--fps", type=float, default=30.00, help="Target frames per second for the compressed videos.")
    parser.add_argument("--duration", type=float, help="Duration to cut the video to (in seconds).")

    args = parser.parse_args()
    
    logger.info("Starting video processing...")
    process_video_files(args.input_dir, args.output_dir, fps=args.fps, codec=args.codec, duration=args.duration)
    logger.info("Video processing completed.")


if __name__ == "__main__":
    main()

# python src/compress_videos.py data/input data/output --fps 24 --codec libx265 --duration 10