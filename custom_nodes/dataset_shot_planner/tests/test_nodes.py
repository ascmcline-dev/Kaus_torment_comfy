from dataset_shot_planner.src.nodes import DatasetShotPlanner, SHOT_VARIANTS

def test_prompt_build():
    node = DatasetShotPlanner()
    result = node.build_prompt(
        "Close-Up Portrait", "45 Degree Left", "Personal Cellphone Photo",
        "Female", "Athletic", "32 B Cup",
        "Neutral", "Natural Daylight", "Plain Neutral",
        "Varied Fitted Outfits", "Standard Dataset", False, 1985, "", "", ""
    )
    assert "45 degrees" in result[0]
    assert "female subject" in result[3]
    assert "32 B Cup" in result[3]
    assert result[7] == "45 Degree Left"
    assert result[8]

def test_chest_ignored_for_non_female():
    node = DatasetShotPlanner()
    result = node.build_prompt(
        "Midshot", "Standing Neutral", "Standard Consumer Camera",
        "Male", "Athletic", "38 DD Cup",
        "Neutral", "Use Style Default", "Unspecified",
        "Fitted Casual", "None", False, 1234, "", "", ""
    )
    assert "38 DD Cup" not in result[3]
    assert "male subject" in result[3]

def test_random_variant():
    node = DatasetShotPlanner()
    result = node.build_prompt(
        "Midshot", "Standing Neutral", "Standard Consumer Camera",
        "Unspecified", "Unspecified", "Unspecified",
        "Neutral", "Use Style Default", "Unspecified",
        "Fitted Casual", "None", True, 1234, "", "", ""
    )
    assert result[7] in SHOT_VARIANTS["Midshot"]
