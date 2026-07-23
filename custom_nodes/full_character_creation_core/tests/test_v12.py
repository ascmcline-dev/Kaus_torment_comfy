import json
from full_character_creation_core.src.nodes import CharacterBlueprintCreator, QwenDatasetQueue, EXPRESSIONS


def build_profile():
    return CharacterBlueprintCreator().build_blueprint(
        gender="Adult Female", age_range="25–34", heritage="Indigenous / Native American",
        skin_tone="Deep Tan", complexion="Natural Skin Texture", face_shape="Oval",
        jaw_shape="Defined", chin_shape="Rounded", eye_color="Gray", eye_shape="Almond",
        eyebrow_shape="Soft Arch", nose_shape="Straight", lip_shape="Balanced Medium",
        hair_color="Medium Brown", hair_length="Mid-Back", hair_texture="Slightly Wavy",
        hair_style="Loose Natural", height="Average", body_type="Average", bust_size="Medium-Full",
        bust_shape="Teardrop", bust_position="Natural Average-Set", bust_firmness="Balanced Natural",
        bust_augmentation="Natural / Unaugmented", buttocks="Average",
        default_clothing="Simple Fitted T-Shirt", jewelry_level="None", tattoo_status="None",
        piercing_status="One", piercing_location="Septum", piercing_type="Horseshoe",
        piercing_material="Black Titanium", piercing_visibility="Documentation",
    )


def test_json_output_and_septum():
    result = build_profile()
    payload = json.loads(result[-1])
    assert payload['schema'] == 'CHARACTER_BLUEPRINT'
    assert 'nasal septum' in payload['marks_prompt']
    assert 'not through either nostril' in payload['marks_prompt']


def test_expression_added():
    assert 'Ahegao (Stylized Adult)' in EXPRESSIONS


def test_qwen_standard_queue_is_40():
    profile = build_profile()[8]
    out = QwenDatasetQueue().build_queue(profile, 'Bootstrap Standard — 40', 1000, 1, 'FCC_Dataset', 'Image 1')
    assert len(out[0]) == 40
    assert out[1][0] == 1000 and out[1][-1] == 1039
    assert all('Edit Image 1' in p for p in out[0])
    manifest = json.loads(out[-1][0])
    assert manifest['total_images'] == 40
