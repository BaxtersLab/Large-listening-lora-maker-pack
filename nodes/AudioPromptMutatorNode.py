class AudioPromptMutatorNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"prompt": ("STRING",), "feedback": ("STRING",)} }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "mutate"
    CATEGORY = "audio_tagging"

    def mutate(self, prompt, feedback):
        # Placeholder: append feedback
        new_prompt = f"{prompt}, improved: {feedback}"
        return (new_prompt,)