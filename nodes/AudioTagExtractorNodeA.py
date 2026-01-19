import subprocess

class AudioTagExtractorNodeA:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"audio_path": ("STRING",)} }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "extract"
    CATEGORY = "audio_tagging"

    def extract(self, audio_path):
        # Call Nexa CLI for semantic audio tags
        result = subprocess.run(['nexa', 'run', 'audiosemantic', '--audio', audio_path, '--prompt', 'Extract semantic tags: instruments, structure, vocals, temporal features'], capture_output=True, text=True)
        tags = result.stdout.strip() if result.returncode == 0 else "Error extracting tags"
        return (tags,)