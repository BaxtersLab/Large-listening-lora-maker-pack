import json


_DEFAULTS = {
    "temperature": 0.8,
    "guidance_scale": 3.0,
    "duration": 30,
    "top_k": 250,
    "top_p": 0.0,
}

_ADJUSTMENTS = {
    "quality":     {"temperature": -0.05, "guidance_scale": +0.3},
    "harsh":       {"temperature": -0.1,  "guidance_scale": -0.2},
    "boring":      {"temperature": +0.1,  "top_k": +50},
    "repetitive":  {"temperature": +0.1,  "top_p": +0.05},
    "too loud":    {"guidance_scale": -0.2},
    "too quiet":   {"guidance_scale": +0.2},
    "accept":      {},
    "revert":      {k: 0 for k in _DEFAULTS},  # sentinel: reset to defaults
    "continue":    {"temperature": +0.02},
}


class AudioParamTunerNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "params_json": ("STRING", {"default": json.dumps(_DEFAULTS, indent=2), "multiline": True}),
                "rationale": ("STRING", {"default": ""}),
                "decision": ("STRING", {"default": "continue"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tuned_params",)
    FUNCTION = "tune"
    CATEGORY = "audio/tagging"

    def tune(self, params_json, rationale, decision):
        try:
            params = json.loads(params_json)
        except json.JSONDecodeError as e:
            return (json.dumps({**_DEFAULTS, "_parse_error": str(e)}, indent=2),)

        if decision == "revert":
            return (json.dumps(_DEFAULTS, indent=2),)

        adjustments = {}
        text = (rationale + " " + decision).lower()
        for keyword, adj in _ADJUSTMENTS.items():
            if keyword in text:
                for k, v in adj.items():
                    adjustments[k] = adjustments.get(k, 0) + v

        clamps = {
            "temperature":    (0.1, 1.5),
            "guidance_scale": (1.0, 10.0),
            "duration":       (5, 300),
            "top_k":          (50, 1000),
            "top_p":          (0.0, 1.0),
        }
        for k, delta in adjustments.items():
            if k in params:
                new_val = params[k] + delta
                if k in clamps:
                    lo, hi = clamps[k]
                    new_val = max(lo, min(hi, new_val))
                params[k] = round(new_val, 4)

        return (json.dumps(params, indent=2),)


NODE_CLASS_MAPPINGS = {"LargeListen_AudioParamTunerNode": AudioParamTunerNode}
NODE_DISPLAY_NAME_MAPPINGS = {"LargeListen_AudioParamTunerNode": "Audio Param Tuner"}
