import importlib.util
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
module_spec = importlib.util.spec_from_file_location(
    "project_emotion_detection",
    project_root / "emotion_detection.py"
)
project_module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(project_module)

detect_emotion = project_module.detect_emotion

__all__ = ["detect_emotion"]
