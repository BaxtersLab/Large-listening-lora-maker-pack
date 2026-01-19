import json
from datetime import datetime

class AudioLoggerNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"audio_path": ("STRING",), "prompt": ("STRING",), "semantic_tags": ("STRING",), "style_tags": ("STRING",), "score": ("FLOAT",), "decision": ("STRING",)} }

    RETURN_TYPES = ()
    FUNCTION = "log"
    CATEGORY = "audio_tagging"
    OUTPUT_NODE = True

    def log(self, audio_path, prompt, semantic_tags, style_tags, score, decision):
        log_entry = {
            "audio": audio_path,
            "prompt": prompt,
            "semantic_tags": semantic_tags.split(', ') if semantic_tags else [],
            "style_tags": style_tags.split(', ') if style_tags else [],
            "score": score,
            "decision": decision,
            "timestamp": datetime.now().isoformat()
        }
        log_file = "audio_tags.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        return ()