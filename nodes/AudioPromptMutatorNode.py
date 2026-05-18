import requests


def _call_llama(server_url, messages, n_predict):
    try:
        resp = requests.post(
            f"{server_url}/chat/completions",
            json={"messages": messages, "max_tokens": n_predict, "temperature": 0.5},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except (requests.RequestException, KeyError, IndexError) as e:
        return f"llama_server_error: {e}"


class AudioPromptMutatorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "", "multiline": True}),
                "rationale": ("STRING", {"default": ""}),
                "server_url": ("STRING", {"default": "http://127.0.0.1:8080/v1"}),
                "n_predict": ("INT", {"default": 200, "min": 50, "max": 1000, "step": 10}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("mutated_prompt",)
    FUNCTION = "mutate"
    CATEGORY = "audio/tagging"

    def mutate(self, prompt, rationale, server_url, n_predict):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert at writing precise audio generation prompts. "
                    "Given a prompt and feedback about which audio tags are missing or mismatched, "
                    "rewrite the prompt to better capture those qualities. "
                    "Return ONLY the improved prompt text, no explanation, no quotes."
                ),
            },
            {
                "role": "user",
                "content": f"Current prompt: {prompt}\n\nFeedback: {rationale}\n\nImproved prompt:",
            },
        ]
        result = _call_llama(server_url, messages, n_predict)
        if result.startswith("llama_server_error"):
            return (prompt,)
        return (result,)


NODE_CLASS_MAPPINGS = {"LargeListen_AudioPromptMutatorNode": AudioPromptMutatorNode}
NODE_DISPLAY_NAME_MAPPINGS = {"LargeListen_AudioPromptMutatorNode": "Audio Prompt Mutator"}
