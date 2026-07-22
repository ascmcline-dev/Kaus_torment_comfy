from full_character_creation_core.src.nodes import CharacterBlueprintCreator, CharacterShotPlanner


def make_profile():
    creator = CharacterBlueprintCreator()
    result = creator.build_blueprint(
        gender="Adult Female", age_range="25–34", heritage="Latin American / Hispanic",
        skin_tone="Deep Tan", complexion="Natural Skin Texture", face_shape="Oval",
        jaw_shape="Defined", chin_shape="Rounded", eye_color="Green", eye_shape="Almond",
        eyebrow_shape="Soft Arch", nose_shape="Straight", lip_shape="Balanced Medium",
        hair_color="Medium Brown", hair_length="Shoulder-Length", hair_texture="Straight",
        hair_style="Center Part", height="Average", body_type="Average", bust_size="Full",
        bust_shape="Round", bust_position="Natural Average-Set", bust_firmness="Balanced Natural",
        bust_augmentation="Natural / Unaugmented", buttocks="Rounded",
        default_clothing="Simple Fitted T-Shirt", jewelry_level="Minimal",
        tattoo_status="One", piercing_status="One",
        tattoo_descriptors="Neck has a black spiderweb tattoo",
        piercing_descriptors="Septum has one metallic horseshoe ring piercing",
    )
    return result


def test_heritage_and_bust_descriptor():
    result = make_profile()
    assert "latin american / hispanic heritage" in result[0].lower()
    assert "full bust" in result[3].lower()
    assert "34" not in result[3]
    assert "cup" not in result[3].lower()


def test_face_stage_excludes_body_and_bust():
    profile = make_profile()[8]
    planner = CharacterShotPlanner()
    result = planner.plan_shot(
        stage="Krea Identity Anchor", shot_type="Face Close-Up", camera_view="Front View",
        pose="Neutral Standing", expression="Neutral", clothing_mode="Profile Default",
        body_region="Upper Torso", background="Plain Neutral", lighting="Soft Natural Daylight",
        photo_style="Authentic Consumer Camera", character_blueprint=profile,
    )
    prompt = result[0].lower()
    assert "septum" in prompt
    assert "spiderweb" in prompt
    assert "full bust" not in prompt
    assert "buttocks" not in prompt


def test_upper_body_stage_includes_bust_not_lower_body():
    profile = make_profile()[8]
    planner = CharacterShotPlanner()
    result = planner.plan_shot(
        stage="Qwen Upper-Body Anchor", shot_type="Waist-Up Midshot", camera_view="Front View",
        pose="Neutral Standing", expression="Neutral", clothing_mode="Profile Default",
        body_region="Upper Torso", background="Plain Neutral", lighting="Soft Natural Daylight",
        photo_style="Identity Documentation", character_blueprint=profile,
    )
    prompt = result[1].lower()
    assert "full bust" in prompt
    assert "buttocks" not in prompt
    assert result[5] == "Portrait Anchor"


def test_clothing_edit_is_authoritative():
    profile = make_profile()[8]
    planner = CharacterShotPlanner()
    result = planner.plan_shot(
        stage="Qwen Clothing Edit", shot_type="Waist-Up Midshot", camera_view="Front View",
        pose="Neutral Standing", expression="Neutral", clothing_mode="Exact Outfit Override",
        body_region="Upper Torso", background="Plain Neutral", lighting="Soft Natural Daylight",
        photo_style="Standard Camera Photo", character_blueprint=profile,
        exact_outfit="opaque fitted black tank top",
    )
    assert "opaque fitted black tank top" in result[1].lower()
    assert "fully worn" in result[1].lower()
