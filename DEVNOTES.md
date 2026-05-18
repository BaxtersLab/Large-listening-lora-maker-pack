# DEVNOTES — Large Listening LoRA Maker
> Carry this file into every future session. It is the handoff document.

---

## Current Status: CODE COMPLETE — AWAITING FIRST TEST

All nodes have been fully rewritten. The pack has never been loaded in ComfyUI.
Next session should start with: **install → load in ComfyUI → smoke test each node.**

---

## What Changed (Session 2 — May 2026)

**Backend switch: Nexa CLI → GGUF Chatbox local server stack**

The original implementation used `nexa run audiosemantic` and `nexa run audiostyle` via subprocess. This was scrapped because Nexa requires models fetched from inside the Nexa app only. Replaced with Baxter's existing GGUF Chatbox app which already runs three local servers.

**Every node was rewritten from scratch:**

| Node | Old state | New state |
|---|---|---|
| `AudioTagExtractorNodeA` | subprocess nexa CLI, no error handling, no IS_CHANGED | Calls listening server (8083) `generate_tags`, formats via chat (8080), IS_CHANGED on file hash |
| `AudioTagExtractorNodeB` | same as A | Same pattern, style-focused LLM prompt |
| `AudioPromptScoreNode` | split on whitespace only — broke with real tag strings | Splits on comma/newline/semicolon, partial word matching, real rationale output |
| `AudioImprovementArbiterNode` | hardcoded 0.1 threshold, one STRING output | Configurable threshold widget, added BOOLEAN `improved` output |
| `AudioPromptMutatorNode` | appended ", improved: {feedback}" literally | Calls chat server (8080) with system+user prompt to genuinely rewrite the prompt |
| `AudioParamTunerNode` | crashed on bad JSON, only adjusted temperature | try/except on JSON parse, adjusts 5 params (temperature/guidance_scale/duration/top_k/top_p), clamped ranges |
| `AudioLoggerNode` | wrote to CWD (unpredictable), returned (), split on ", " only | Writes to `<pack>/logs/audio_tags.jsonl`, returns UI dict, robust tag splitting |
| `NexaPopupLoaderNode` | tkinter mainloop() blocked ComfyUI server thread | **Deleted.** Replaced with `LlamaCppServerNode` |
| `LlamaCppServerNode` | did not exist | New node: health-pings all 3 servers, outputs chat_url / listening_url / vision_url |

**Other files changed:**
- `__init__.py` — updated imports, all keys prefixed `LargeListen_` to avoid global collisions
- `requirements.txt` — was `torch, numpy, nexa-cli` → now just `requests`
- `examples/sample_workflow.json` — was invalid format (wrong link structure, wrong node format) → fully rewritten as valid ComfyUI workflow JSON, drag-and-drop ready
- `NexaPopupLoaderNode.py` — left on disk but no longer imported (safe to delete)

---

## Server Architecture (do not change these ports — they are fixed by GGUF Chatbox)

| Server | Port | API style | Use for |
|---|---|---|---|
| Chat/Text proxy | 8080 | `POST /v1/chat/completions` (OpenAI) | LLM text generation, prompt mutation, tag formatting |
| Vision (llava) | 8082 | `POST /v1/chat/completions` (OpenAI) | Image understanding (not used by this pack yet) |
| Listening (audio) | 8083 | `POST /action` (custom) | Audio analysis: musicnn tags, mutagen metadata, Whisper transcription |

Full protocol reference: `c:\Users\Baxter\Desktop\rag libary\baxter-server-connections.md`

---

## What Still Needs Doing

### Priority 1 — Must do before this pack is usable

- [ ] **Smoke test in ComfyUI** — load the pack, confirm no import errors in the console
- [ ] **Test LlamaCppServerNode** — start GGUF Chatbox, add the node, confirm status shows `online` for chat and listening
- [ ] **Test AudioTagExtractorA** — point at a real .wav file, confirm listening server responds and tags come back
- [ ] **Test AudioTagExtractorB** — same
- [ ] **Test the full sample workflow** — drag `examples/sample_workflow.json` into ComfyUI, wire up a real audio path, run it end to end
- [ ] **Verify AudioLoggerNode writes to `logs/audio_tags.jsonl`** — check the file exists and entries are valid JSON

### Priority 2 — Improvements once basic flow works

- [ ] **Add an audio generation node** — the pack scores and mutates prompts but has no node to actually generate audio. AudioCraft or a compatible backend needs to be wired in. This is the missing link for a true generate→score→mutate loop.
- [ ] **Add a `transcribe` action node** — `AudioTagExtractorA/B` only uses `generate_tags`. A separate `AudioTranscribeNode` calling `POST 8083/action` with `action: "transcribe"` would add lyrics/speech to the dataset.
- [ ] **Connect AudioParamTunerNode into the sample workflow** — it was built but not wired into `sample_workflow.json` to keep the example readable. Add it between Arbiter and Logger.
- [ ] **Test AudioPromptMutatorNode with a live chat server** — confirm the LLM actually rewrites the prompt meaningfully, not just echoes it
- [ ] **Add `vision_url` usage** — LlamaCppServerNode exposes vision_url but nothing uses it yet. Future: a node that takes a spectrogram image and feeds it to the vision server.

### Priority 3 — Polish

- [ ] **Update README.md** — still describes the old Nexa architecture. Needs to reflect the GGUF Chatbox server setup.
- [ ] **Delete NexaPopupLoaderNode.py** — it's a dead file. Safe to remove once confirmed nothing references it.
- [ ] **Add `pyproject.toml`** — missing from the pack. Add with proper ComfyUI registry metadata.

---

## Known Risks / Watch Out For

- **Both GGUF Chatbox servers must be running** before any node that calls them is queued. If the chat or listening server is offline, nodes return an error string rather than crashing — this is intentional and safe, but the workflow result will be empty/garbage. Add the `LlamaCppServerNode` to your workflow and check its `status` output first.
- **`file_path` to listening server must be absolute.** Relative paths return an error. Always use full paths like `C:/Users/Baxter/audio/track.wav`.
- **`IS_CHANGED` on extractors hashes the first 64KB of the audio file.** If you replace a file in-place with a different audio at the same path, it will correctly re-run. If the file doesn't exist yet, it falls back to `float("nan")` (always re-run).
- **`AudioParamTunerNode` expects valid JSON** in `params_json`. If it gets garbage, it returns a dict with the parse error and resets to defaults — it will not crash ComfyUI.
- **Log file location:** `<pack_root>/logs/audio_tags.jsonl` — created automatically on first run. The `logs/` dir is created if missing.

---

## Node Key Names (for workflow JSON)

All keys are prefixed `LargeListen_` to prevent collision with other packs.

| Key (in workflow JSON `type` field) | Display name |
|---|---|
| `LargeListen_LlamaCppServerNode` | GGUF Chatbox Servers |
| `LargeListen_AudioTagExtractorA` | Audio Tag Extractor A (Semantic) |
| `LargeListen_AudioTagExtractorB` | Audio Tag Extractor B (Style) |
| `LargeListen_AudioPromptScoreNode` | Audio Prompt Score |
| `LargeListen_AudioImprovementArbiterNode` | Audio Improvement Arbiter |
| `LargeListen_AudioPromptMutatorNode` | Audio Prompt Mutator |
| `LargeListen_AudioParamTunerNode` | Audio Param Tuner |
| `LargeListen_AudioLoggerNode` | Audio Logger |

---

## Session Log

| Date | What happened |
|---|---|
| ~4 months ago | Initial build with GPT-4o mini. Nexa CLI backend. Placeholders throughout. Workflow JSON was invalid format. |
| 2026-05-18 | Full rewrite with Claude. Switched to GGUF Chatbox server stack (8080/8082/8083). All nodes functional. Workflow JSON fixed. Server connection guide written to RAG library. |
