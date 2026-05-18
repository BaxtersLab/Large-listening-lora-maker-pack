class AudioImprovementArbiterNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "current_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "previous_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "threshold": ("FLOAT", {"default": 0.05, "min": 0.01, "max": 0.5, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("decision", "improved")
    FUNCTION = "decide"
    CATEGORY = "audio/tagging"

    def decide(self, current_score, previous_score, threshold):
        delta = current_score - previous_score
        if delta > threshold:
            return ("accept", True)
        elif delta < -threshold:
            return ("revert", False)
        else:
            return ("continue", current_score >= previous_score)


NODE_CLASS_MAPPINGS = {"LargeListen_AudioImprovementArbiterNode": AudioImprovementArbiterNode}
NODE_DISPLAY_NAME_MAPPINGS = {"LargeListen_AudioImprovementArbiterNode": "Audio Improvement Arbiter"}
