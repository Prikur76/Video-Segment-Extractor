import os

from typing import Dict
from moviepy import VideoFileClip

from utils.label_utils import categorize_label
from utils.app_logger import get_logger

logger = get_logger(__name__)


class VideoSegmentProcessor:
    def process(self, args) -> None:
        """
        Обрабатывает один фрагмент, извлекая его из видеоклипа и сохраняя на диск.
        """
        clip_path, segment, output_dir, cam_idx, segment_idx, codec, fps = args
        
        with VideoFileClip(clip_path) as clip:
            label = segment["label"]
            start = segment["start"]
            end = segment["end"]
            clip_start = max(0, start - clip.start)
            clip_end = min(end - clip.start, clip.duration)

            if clip_start < clip_end:
                # Определяем категорию метки
                category = categorize_label(label)
                
                # Создаем путь для сохранения
                save_dir = os.path.join(
                    output_dir,  # Основная папка (например, data/output/20241123_194318)
                    category,   # Категория (kata, combinations, elements)
                    label,      # Название метки (например, Heian-Nidan)
                    str(segment_idx)  # Номер сегмента (например, 1)
                )
                os.makedirs(save_dir, exist_ok=True)
                
                # Формируем имя файла
                segment_filename = f"cam{cam_idx}_{segment_idx}.mp4"
                segment_path = os.path.join(save_dir, segment_filename)
                print(segment_path)

                # Сохраняем сегмент
                segment_clip = clip.subclipped(clip_start, clip_end)
                try:
                    segment_clip.write_videofile(segment_path, codec=codec, fps=fps, logger=None)  # logger=None suppresses logging
                    logger.info(f"Segment {segment_path} saved successfully.")
                except Exception as e:
                    logger.error(f"Error processing segment {label}: {e}")
            else:
                logger.warning(f"Segment {label} is out of bounds for camera {cam_idx}")
