from .src.nodes import CharacterBlueprintCreator, CharacterShotPlanner

NODE_CLASS_MAPPINGS = {
    "CharacterBlueprintCreator": CharacterBlueprintCreator,
    "CharacterShotPlanner": CharacterShotPlanner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CharacterBlueprintCreator": "Character Blueprint Creator v1.0",
    "CharacterShotPlanner": "Character Shot Planner v1.0",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
