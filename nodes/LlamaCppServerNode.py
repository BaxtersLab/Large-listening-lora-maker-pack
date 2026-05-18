import requests


def _ping(base_url, timeout=3):
    try:
        resp = requests.get(f"{base_url}/health", timeout=timeout)
        return "online" if resp.status_code == 200 else f"HTTP {resp.status_code}"
    except requests.ConnectionError:
        return "offline"
    except requests.Timeout:
        return "timeout"
    except requests.RequestException as e:
        return f"error: {e}"


class LlamaCppServerNode:
    """
    Central config node for the GGUF Chatbox server stack.
    Wire chat_url / listening_url / vision_url outputs into any node
    that needs to call a server, so you configure the host in one place.

    Ports (fixed by the app):
      8080 → chat/text proxy (OpenAI-compatible /v1)
      8082 → vision server  (OpenAI-compatible /v1)
      8083 → listening server (custom /action endpoint)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "host": ("STRING", {"default": "127.0.0.1"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("chat_url", "listening_url", "vision_url", "status")
    FUNCTION = "check"
    CATEGORY = "audio/llama"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def check(self, host):
        chat_url = f"http://{host}:8080/v1"
        listening_url = f"http://{host}:8083"
        vision_url = f"http://{host}:8082/v1"

        chat_status = _ping(f"http://{host}:8080")
        listening_status = _ping(f"http://{host}:8083")
        vision_status = _ping(f"http://{host}:8082")

        status = (
            f"chat:{chat_status} | listening:{listening_status} | vision:{vision_status}"
        )
        return (chat_url, listening_url, vision_url, status)


NODE_CLASS_MAPPINGS = {"LargeListen_LlamaCppServerNode": LlamaCppServerNode}
NODE_DISPLAY_NAME_MAPPINGS = {"LargeListen_LlamaCppServerNode": "GGUF Chatbox Servers"}
