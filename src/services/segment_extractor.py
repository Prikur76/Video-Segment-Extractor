import os

from multiprocessing import Pool, cpu_count
from moviepy import VideoFileClip

from utils.decorators import timer
from utils.app_logger import get_logger


logger = get_logger(__name__)


class LabeledSegmentsExtractor:
    def __init__(self, config_loader, annotation_loader, segment_processor):
        self.config_loader = config_loader
        self.annotation_loader = annotation_loader
        self.segment_processor = segment_processor

    @timer
    def extract(self, config_path: str) -> None:
        """Обрабатывает все конфигурации из файла."""
        configs = self.config_loader.load(config_path)  # Загружаем список конфигураций

        for config in configs:
            self._process_single_config(config)
    
    def _process_single_config(self, config: dict) -> None:
        """Обрабатывает одну конфигурацию."""
        video_paths = config["video_paths"]
        annotation_path = config["json_path"]
        output_dir = config["output_dir"]  # Основная папка для конфигурации
        frame_offsets = config["frame_offsets"]
        codec = config["codec"]
        fps = config["fps"]
        execution_mode = config.get("execution_mode", "parallel")

        os.makedirs(output_dir, exist_ok=True)

        for camera_index, (video_path, frame_offset) in enumerate(zip(video_paths, frame_offsets), start=1):
            with VideoFileClip(video_path) as video_clip:
                segments = self.annotation_loader.load(annotation_path, video_clip.fps, frame_offset)

            label_to_segments = {}
            for segment in segments:
                label = segment["label"]
                if label not in label_to_segments:
                    label_to_segments[label] = []
                label_to_segments[label].append(segment)

            for label, segments in label_to_segments.items():
                args_list = [(video_path, segment, output_dir, camera_index, segment_idx, codec, fps)
                             for segment_idx, segment in enumerate(segments, start=1)]

                if execution_mode == "parallel":
                    # Многопоточное выполнение
                    with Pool(processes=cpu_count()) as pool:
                        pool.map(self.segment_processor.process, args_list)
                else:
                    # Последовательное выполнение
                    for args in args_list:
                        self.segment_processor.process(args)

        logger.info(f"Обработка завершена для конфигурации: {config['video_dataset']}")
