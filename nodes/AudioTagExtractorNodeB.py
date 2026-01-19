import subprocess

class AudioTagExtractorNodeB:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"audio_path": ("STRING",)} }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "extract"
    CATEGORY = "audio_tagging"

    def extract(self, audio_path):
        # Call Nexa CLI for style audio tags
        result = subprocess.run(['nexa', 'run', 'audiostyle', '--audio', audio_path, '--prompt', 'Extract style tags: genre, production style, texture, stereo width, aesthetic features'], capture_output=True, text=True)
        tags = result.stdout.strip() if result.returncode == 0 else "Error extracting tags"
        return (tags,)