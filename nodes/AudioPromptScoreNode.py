import re


def _parse_tags(tag_string):
    parts = re.split(r"[,\n;]+", tag_string)
    return set(p.strip().lower() for p in parts if len(p.strip()) > 1)


class AudioPromptScoreNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "semantic_tags": ("STRING", {"default": ""}),
                "style_tags": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("FLOAT", "STRING")
    RETURN_NAMES = ("score", "rationale")
    FUNCTION = "score_prompt"
    CATEGORY = "audio/tagging"

    def score_prompt(self, prompt, semantic_tags, style_tags):
        if not prompt.strip():
            return (0.0, "Empty prompt — score is 0")

        prompt_words = set(w.lower() for w in re.split(r"\W+", prompt) if len(w) > 2)
        all_tags = _parse_tags(semantic_tags) | _parse_tags(style_tags)

        if not all_tags:
            return (0.0, "No tags extracted — cannot score")

        direct_hits = prompt_words & all_tags

        partial_hits = set()
        for pw in prompt_words:
            for tag in all_tags:
                if pw in tag or tag in pw:
                    partial_hits.add(pw)
        partial_hits -= direct_hits

        direct_score = len(direct_hits) / max(len(prompt_words), 1)
        partial_score = len(partial_hits) / max(len(prompt_words), 1) * 0.5
        coverage = (len(direct_hits) + len(partial_hits)) / max(len(all_tags), 1) * 0.3
        score = min(1.0, direct_score + partial_score + coverage)

        missing = all_tags - prompt_words - partial_hits
        rationale = (
            f"Score: {score:.2f} | Direct matches: {sorted(direct_hits)} | "
            f"Partial matches: {sorted(partial_hits)} | "
            f"Missing from prompt: {sorted(list(missing)[:5])}"
        )
        return (float(score), rationale)


NODE_CLASS_MAPPINGS = {"LargeListen_AudioPromptScoreNode": AudioPromptScoreNode}
NODE_DISPLAY_NAME_MAPPINGS = {"LargeListen_AudioPromptScoreNode": "Audio Prompt Score"}
