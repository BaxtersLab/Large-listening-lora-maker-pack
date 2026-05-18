import json
import re
from datetime import datetime
from pathlib import Path

_LOG_DIR = Path(__file__).parent.parent / "logs"


def _parse_tags(tag_string):
    parts = re.split(r"[,\n;]+", tag_string)
    return [p.strip() for p in parts if p.strip()]


class AudioLoggerNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio_path": ("STRING", {"default": ""}),
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "semantic_tags": ("STRING", {"default": ""}),
                "style_tags": ("STRING", {"default": ""}),
                "score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                "decision": ("STRING", {"default": "continue"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "log_entry"
    CATEGORY = "audio/tagging"
    OUTPUT_NODE = True

    def log_entry(self, audio_path, prompt, semantic_tags, style_tags, score, decision):
        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = _LOG_DIR / "audio_tags.jsonl"

        entry = {
            "timestamp": datetime.now().isoformat(),
            "audio": audio_path,
            "prompt": prompt,
            "semantic_tags": _parse_tags(semantic_tags),
            "style_tags": _parse_tags(style_tags),
            "score": round(float(score), 4),
            "decision": decision,
        }

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

        return {"ui": {"text": [f"Logged [{decision}] score={score:.3f} → {log_file}"]}}


NODE_CLASS_MAPPINGS = {"LargeListen_AudioLoggerNode": AudioLoggerNode}
NODE_DISPLAY_NAME_MAPPINGS = {"LargeListen_AudioLoggerNode": "Audio Logger"}
