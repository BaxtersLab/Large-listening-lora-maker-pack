class AudioImprovementArbiterNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"current_score": ("FLOAT",), "previous_score": ("FLOAT",)} }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "decide"
    CATEGORY = "audio_tagging"

    def decide(self, current_score, previous_score):
        if current_score > previous_score + 0.1:
            decision = "accept"
        elif current_score < previous_score:
            decision = "revert"
        else:
            decision = "continue"
        return (decision,)