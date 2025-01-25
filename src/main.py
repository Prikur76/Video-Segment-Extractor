from loaders.config_loader import JsonConfigLoader, YamlConfigLoader
from loaders.annotation_loader import AnnotationLoader
from processors.video_processor import VideoSegmentProcessor
from services.segment_extractor import LabeledSegmentsExtractor


if __name__ == "__main__":
    config_loader = YamlConfigLoader()
    annotation_loader = AnnotationLoader()
    segment_processor = VideoSegmentProcessor()
    
    extractor = LabeledSegmentsExtractor(config_loader, annotation_loader, segment_processor)

    extractor.extract("configs/config.yaml")
