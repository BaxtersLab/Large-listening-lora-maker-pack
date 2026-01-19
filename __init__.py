from .nodes.AudioTagExtractorNodeA import AudioTagExtractorNodeA
from .nodes.AudioTagExtractorNodeB import AudioTagExtractorNodeB
from .nodes.AudioPromptScoreNode import AudioPromptScoreNode
from .nodes.AudioImprovementArbiterNode import AudioImprovementArbiterNode
from .nodes.AudioPromptMutatorNode import AudioPromptMutatorNode
from .nodes.AudioParamTunerNode import AudioParamTunerNode
from .nodes.AudioLoggerNode import AudioLoggerNode

NODE_CLASS_MAPPINGS = {
    "AudioTagExtractorNodeA": AudioTagExtractorNodeA,
    "AudioTagExtractorNodeB": AudioTagExtractorNodeB,
    "AudioPromptScoreNode": AudioPromptScoreNode,
    "AudioImprovementArbiterNode": AudioImprovementArbiterNode,
    "AudioPromptMutatorNode": AudioPromptMutatorNode,
    "AudioParamTunerNode": AudioParamTunerNode,
    "AudioLoggerNode": AudioLoggerNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AudioTagExtractorNodeA": "Audio Tag Extractor A (Semantic)",
    "AudioTagExtractorNodeB": "Audio Tag Extractor B (Style)",
    "AudioPromptScoreNode": "Audio Prompt Score",
    "AudioImprovementArbiterNode": "Audio Improvement Arbiter",
    "AudioPromptMutatorNode": "Audio Prompt Mutator",
    "AudioParamTunerNode": "Audio Param Tuner",
    "AudioLoggerNode": "Audio Logger",
}