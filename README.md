# Large Listening LoRA Maker

A ComfyUI extension for autonomous audio refinement and tagging using dual [LLM + Audio] stacks.

## Purpose

Analyze generated audio, extract semantic and stylistic tags, refine prompts and parameters, and build datasets for LoRA training in genre-specific audio generation.

## Features

- **AudioCraft Integration**: Generates audio via compatible backend.
- **Dual Nexa CLI Instances**:
  - `nexaaudiosemantic`: Semantic-focused (instruments, structure, vocals)
  - `nexaaudiostyle`: Style-focused (genre, production, texture)
- **Iterative Loop**: Generate → Extract Tags → Score → Mutate → Repeat
- **Modular Nodes**: Classes for mutation, tuning, extraction, scoring, arbitration, logging

## Installation

1. **Clone or Download**: Get the project files.
2. **Python Environment**:
   - Install Python 3.10+
   - Create venv: `python -m venv .venv`
   - Activate: `.venv\Scripts\activate` (Windows)
3. **Install Dependencies**:
   - `pip install -r requirements.txt`
4. **Install AudioCraft**:
   - Follow https://github.com/facebookresearch/audiocraft
   - Or compatible audio generator.
5. **Install Nexa CLI**:
   - `pip install nexa-cli`
   - Pull models: `nexa pull audiosemantic` and `nexa pull audiostyle`

## Usage

1. **Start Services**:
   - Launch AudioCraft or compatible generator.
   - Ensure Nexa models are ready.

2. **Run in ComfyUI**:
   - Load the extension.
   - Use sample workflow in examples/ and connect audio paths.

3. **Monitor**:
   - Check `audio_tags.jsonl` for logs.

## Workflow Details

- **Initial Setup**: Prompt and params (duration, temperature, etc.).
- **Loop (Max 10 iterations)**:
  1. Generate audio via backend.
  2. Extract semantic tags (audiosemantic) and style tags (audiostyle).
  3. Score alignment.
  4. If improved, accept; else mutate prompt/params.
- **Output**: Final audio, log of iterations.

## Nodes Overview

### AudioTagExtractorNodeA
- **Input**: Audio path (string)
- **Output**: Semantic tags (string)
- **Function**: Extracts semantic tags using nexaaudiosemantic.

### AudioTagExtractorNodeB
- **Input**: Audio path (string)
- **Output**: Style tags (string)
- **Function**: Extracts style tags using nexaaudiostyle.

### AudioPromptScoreNode
- **Inputs**: Prompt (string), Semantic tags (string), Style tags (string)
- **Outputs**: Score (float), Rationale (string)
- **Function**: Scores prompt-audio alignment.

### AudioImprovementArbiterNode
- **Inputs**: Current score (float), Previous score (float)
- **Output**: Decision (string)
- **Function**: Decides to accept, revert, or continue.

### AudioPromptMutatorNode
- **Inputs**: Prompt (string), Feedback (string)
- **Output**: New prompt (string)
- **Function**: Revises prompt based on feedback.

### AudioParamTunerNode
- **Inputs**: Params (string JSON), Feedback (string)
- **Output**: New params (string JSON)
- **Function**: Adjusts parameters.

### AudioLoggerNode
- **Inputs**: Audio path, prompt, tags, score, decision
- **Output**: None (logs to file)
- **Function**: Logs to `audio_tags.jsonl`.

## Outputs

- **audio_tags.jsonl**: JSON Lines with entries like:
  ```json
  {
    "audio": "audio_001.wav",
    "prompt": "jazz piano solo",
    "semantic_tags": ["piano", "solo"],
    "style_tags": ["jazz"],
    "score": 0.8,
    "decision": "accept",
    "timestamp": "2026-01-18T12:00:00Z"
  }
  ```

## Dependencies

- AudioCraft or compatible
- Nexa CLI with audiosemantic and audiostyle
- Python: torch, numpy

## Troubleshooting

- Ensure audio generator is running.
- Check Nexa CLI for model availability.
- Logs in `audio_tags.jsonl` for debugging.

## License

MIT