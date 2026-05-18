from .nodes.AudioTagExtractorNodeA import AudioTagExtractorNodeA
from .nodes.AudioTagExtractorNodeB import AudioTagExtractorNodeB
from .nodes.AudioPromptScoreNode import AudioPromptScoreNode
from .nodes.AudioImprovementArbiterNode import AudioImprovementArbiterNode
from .nodes.AudioPromptMutatorNode import AudioPromptMutatorNode
from .nodes.AudioParamTunerNode import AudioParamTunerNode
from .nodes.AudioLoggerNode import AudioLoggerNode
from .nodes.LlamaCppServerNode import LlamaCppServerNode

NODE_CLASS_MAPPINGS = {
    "LargeListen_AudioTagExtractorA": AudioTagExtractorNodeA,
    "LargeListen_AudioTagExtractorB": AudioTagExtractorNodeB,
    "LargeListen_AudioPromptScoreNode": AudioPromptScoreNode,
    "LargeListen_AudioImprovementArbiterNode": AudioImprovementArbiterNode,
    "LargeListen_AudioPromptMutatorNode": AudioPromptMutatorNode,
    "LargeListen_AudioParamTunerNode": AudioParamTunerNode,
    "LargeListen_AudioLoggerNode": AudioLoggerNode,
    "LargeListen_LlamaCppServerNode": LlamaCppServerNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LargeListen_AudioTagExtractorA": "Audio Tag Extractor A (Semantic)",
    "LargeListen_AudioTagExtractorB": "Audio Tag Extractor B (Style)",
    "LargeListen_AudioPromptScoreNode": "Audio Prompt Score",
    "LargeListen_AudioImprovementArbiterNode": "Audio Improvement Arbiter",
    "LargeListen_AudioPromptMutatorNode": "Audio Prompt Mutator",
    "LargeListen_AudioParamTunerNode": "Audio Param Tuner",
    "LargeListen_AudioLoggerNode": "Audio Logger",
    "LargeListen_LlamaCppServerNode": "GGUF Chatbox Servers",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
