import json

from typing import Dict, List, Union


class AnnotationLoader:
    def load(self, json_path: str, fps: float, start_offset: int = 0) -> List[Dict[str, Union[str, float]]]:
        with open(json_path, "r") as f:
            annotations = json.load(f)
        
        segments = []
        for video_label in annotations[0]["videoLabels"]:
            for range_ in video_label["ranges"]:
                start_frame = range_["start"] + start_offset
                end_frame = range_["end"] + start_offset
                label = video_label["timelinelabels"][0]
                start_time = start_frame / fps
                end_time = end_frame / fps
                segments.append({"label": label, "start": start_time, "end": end_time})
        return segments
