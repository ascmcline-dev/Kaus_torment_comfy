from .src.nodes import CharacterBlueprintCreator, CharacterShotPlanner, QwenDatasetQueue

NODE_CLASS_MAPPINGS = {
    "CharacterBlueprintCreator": CharacterBlueprintCreator,
    "CharacterShotPlanner": CharacterShotPlanner,
    "QwenDatasetQueue": QwenDatasetQueue,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CharacterBlueprintCreator": "Character Blueprint Creator v1.2",
    "CharacterShotPlanner": "Character Shot Planner v1.2",
    "QwenDatasetQueue": "FCC Qwen Dataset Queue v1.0",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
