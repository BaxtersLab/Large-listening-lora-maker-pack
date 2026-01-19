class AudioPromptScoreNode:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"prompt": ("STRING",), "semantic_tags": ("STRING",), "style_tags": ("STRING",)} }

    RETURN_TYPES = ("FLOAT", "STRING")
    RETURN_NAMES = ("score", "rationale")
    FUNCTION = "score"
    CATEGORY = "audio_tagging"

    def score(self, prompt, semantic_tags, style_tags):
        # Placeholder: simple overlap score
        prompt_words = set(word.lower() for word in prompt.split() if len(word) > 2)
        all_tags = (semantic_tags + ' ' + style_tags).split()
        tag_words = set(tag.lower() for tag in all_tags)
        overlap = len(prompt_words & tag_words)
        score = overlap / len(prompt_words) if prompt_words else 0
        rationale = f"Overlap: {overlap}/{len(prompt_words)}"
        return (score, rationale)