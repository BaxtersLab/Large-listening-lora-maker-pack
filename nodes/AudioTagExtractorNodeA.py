import requests
import json


def _get_audio_analysis(listening_url, audio_path):
    try:
        resp = requests.post(
            f"{listening_url}/action",
            json={"action": "generate_tags", "file_path": audio_path},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            return None, f"listening server returned error: {data}"
        return data, None
    except requests.RequestException as e:
        return None, f"listening_server_error: {e}"


def _call_chat(chat_url, system_msg, user_msg, n_predict):
    try:
        resp = requests.post(
            f"{chat_url}/chat/completions",
            json={
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                "max_tokens": n_predict,
                "temperature": 0.3,
            },
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except (requests.RequestException, KeyError, IndexError) as e:
        return f"chat_server_error: {e}"


class AudioTagExtractorNodeA:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio_path": ("STRING", {"default": ""}),
                "listening_url": ("STRING", {"default": "http://127.0.0.1:8083"}),
                "chat_url": ("STRING", {"default": "http://127.0.0.1:8080/v1"}),
                "n_predict": ("INT", {"default": 300, "min": 50, "max": 2000, "step": 10}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("semantic_tags",)
    FUNCTION = "extract"
    CATEGORY = "audio/tagging"

    @classmethod
    def IS_CHANGED(cls, audio_path, **kwargs):
        import hashlib
        try:
            return hashlib.md5(open(audio_path, "rb").read(65536)).hexdigest()
        except Exception:
            return float("nan")

    def extract(self, audio_path, listening_url, chat_url, n_predict):
        data, err = _get_audio_analysis(listening_url, audio_path)
        if err:
            return (err,)

        raw = json.dumps(
            {"tags": data.get("tags", {}), "ai_tags": data.get("ai_tags", {})},
            indent=2,
        )
        system_msg = (
            "You are an expert audio analyst. Given raw audio analysis data from a music file, "
            "output ONLY a comma-separated list of semantic tags describing: "
            "instruments present, song structure (verse/chorus/bridge/intro/outro/solo), "
            "vocal presence and style (male/female/harmonies/none), rhythmic complexity, "
            "tempo feel, and harmonic character. "
            "No explanations, no bullet points — only the comma-separated tags."
        )
        user_msg = f"File: {audio_path}\n\nAnalysis data:\n{raw}\n\nSemantic tags:"
        tags = _call_chat(chat_url, system_msg, user_msg, n_predict)
        return (tags,)


NODE_CLASS_MAPPINGS = {"LargeListen_AudioTagExtractorA": AudioTagExtractorNodeA}
NODE_DISPLAY_NAME_MAPPINGS = {"LargeListen_AudioTagExtractorA": "Audio Tag Extractor A (Semantic)"}
