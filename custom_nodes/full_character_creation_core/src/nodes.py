from __future__ import annotations

import hashlib
import re
from typing import Any


def _join(*parts: str) -> str:
    return ", ".join(str(p).strip(" ,") for p in parts if p and str(p).strip(" ,"))


def _slug(text: str) -> str:
    value = str(text).lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


GENDERS = ["Adult Female", "Adult Male", "Adult Nonbinary"]
AGE_RANGES = ["18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
HERITAGES = [
    "Unspecified",
    "Latin American / Hispanic",
    "Afro-Latino",
    "Caribbean",
    "White / European (Caucasian)",
    "Mediterranean / Southern European",
    "Black / African Descent",
    "Mixed Black / Multiracial",
    "East Asian",
    "Japanese",
    "Chinese",
    "Korean",
    "South Asian",
    "Southeast Asian",
    "Middle Eastern / North African",
    "Indigenous / Native American",
    "Pacific Islander",
    "Mixed Heritage",
    "Custom",
]
SKIN_TONES = [
    "Very Light", "Light", "Light-Medium", "Medium", "Olive", "Deep Tan",
    "Brown", "Deep Brown", "Very Deep", "Custom / Unspecified",
]
COMPLEXIONS = [
    "Natural Skin Texture", "Clear and Even", "Freckled", "Lightly Freckled",
    "Visible Pores", "Sun-Kissed", "Mature Natural Skin", "Unspecified",
]
FACE_SHAPES = ["Oval", "Round", "Heart-Shaped", "Soft Angular", "Square", "Long", "Diamond", "Unspecified"]
JAW_SHAPES = ["Delicate", "Soft", "Defined", "Strong", "Wide", "Tapered", "Unspecified"]
CHIN_SHAPES = ["Rounded", "Pointed", "Square", "Soft", "Prominent", "Unspecified"]
EYE_COLORS = ["Brown", "Dark Brown", "Hazel", "Green", "Blue", "Gray", "Amber", "Custom / Unspecified"]
EYE_SHAPES = ["Almond", "Round", "Prominent", "Deep-Set", "Hooded", "Upturned", "Downturned", "Unspecified"]
EYEBROWS = ["Soft Arch", "High Arch", "Straight", "Thick Natural", "Thin Natural", "Angular", "Unspecified"]
NOSES = ["Straight", "Narrow", "Button", "Wide", "Aquiline", "Rounded", "Upturned", "Unspecified"]
LIPS = ["Thin", "Balanced Medium", "Full", "Soft Cupid's Bow", "Wide", "Narrow", "Unspecified"]
HAIR_COLORS = ["Black", "Dark Brown", "Medium Brown", "Light Brown", "Strawberry Blonde", "Blonde", "Platinum", "Red", "Gray", "Silver", "Custom"]
HAIR_LENGTHS = ["Buzzed", "Very Short", "Chin-Length", "Shoulder-Length", "Mid-Back", "Waist-Length", "Custom"]
HAIR_TEXTURES = ["Pin-Straight", "Straight", "Slightly Wavy", "Wavy", "Curly", "Coily", "Custom"]
HAIR_STYLES = ["Loose Natural", "Center Part", "Side Part", "Braids", "Ponytail", "Bun", "Pixie", "Locs", "Afro", "Custom"]
HEIGHTS = ["Short", "Below Average", "Average", "Above Average", "Tall", "Very Tall", "Unspecified"]
BODY_TYPES = ["Very Slim", "Slim", "Average", "Athletic", "Curvy", "Full-Figured", "Muscular", "Heavyset", "Custom / Unspecified"]
BUST_SIZES = [
    "Unspecified", "Very Small", "Small", "Small-Medium", "Medium",
    "Medium-Full", "Full", "Large", "Very Large", "Overly Large",
]
BUST_SIZE_PROMPTS = {
    "Very Small": "very small bust with minimal projection and subtle chest volume",
    "Small": "small bust with gentle natural projection",
    "Small-Medium": "small-to-medium bust with modest natural projection",
    "Medium": "medium bust with balanced natural projection",
    "Medium-Full": "medium-full bust with noticeable but balanced projection",
    "Full": "full bust with pronounced natural volume and projection",
    "Large": "large bust with substantial natural volume and projection",
    "Very Large": "very large bust with heavy natural volume and strong projection",
    "Overly Large": "extremely large bust with exaggerated volume, very strong projection, and substantial natural weight",
}
BUST_SHAPES = ["Unspecified", "Bell Shape", "Teardrop", "Round", "Asymmetrical Natural", "East-West", "Side-Set", "Slender"]
BUST_SHAPE_PROMPTS = {
    "Bell Shape": "bell-shaped bust with a narrower upper pole and fuller rounded lower pole",
    "Teardrop": "teardrop-shaped bust with a gentle upper slope and natural lower fullness",
    "Round": "round bust with balanced upper-pole and lower-pole fullness",
    "Asymmetrical Natural": "naturally asymmetrical bust with subtle realistic left-right variation",
    "East-West": "east-west bust orientation with projection angled slightly outward",
    "Side-Set": "side-set bust with a wider natural center gap and fuller outer chest",
    "Slender": "slender elongated bust shape with a narrow base and gentle vertical contour",
}
BUST_POSITIONS = ["Unspecified", "Natural Average-Set", "High-Set / Perky", "High and Tight", "Low-Set", "Downward-Sloping", "Pendulous Natural"]
BUST_POSITION_PROMPTS = {
    "Natural Average-Set": "natural average-set chest position",
    "High-Set / Perky": "high-set perky chest position with a natural upward presentation",
    "High and Tight": "high and tight chest position with compact attachment and minimal lower drop",
    "Low-Set": "low-set chest position with realistic gravitational weight",
    "Downward-Sloping": "natural downward-sloping chest position with visible lower-pole weight",
    "Pendulous Natural": "naturally pendulous chest position with lower-set fullness and realistic gravitational drop",
}
BUST_FIRMNESS = ["Unspecified", "Firm", "Naturally Firm", "Balanced Natural", "Soft", "Very Soft / Natural Movement"]
BUST_FIRMNESS_PROMPTS = {
    "Firm": "firm chest tissue with limited natural movement",
    "Naturally Firm": "naturally firm chest tissue with stable shape and slight realistic movement",
    "Balanced Natural": "balanced natural chest tissue with moderate softness and realistic weight",
    "Soft": "soft natural chest tissue with gentle shape variation and realistic gravity",
    "Very Soft / Natural Movement": "very soft natural chest tissue with pronounced settling, weight, and realistic movement",
}
BUST_AUGMENTATION = ["Unspecified", "Natural / Unaugmented", "Subtle Natural-Looking Augmentation", "Round High-Profile Implants", "Teardrop / Anatomical Implants", "Very Firm Augmented Projection"]
BUST_AUGMENTATION_PROMPTS = {
    "Natural / Unaugmented": "natural unaugmented chest structure",
    "Subtle Natural-Looking Augmentation": "subtle natural-looking augmentation with moderate projection and preserved natural slope",
    "Round High-Profile Implants": "round high-profile implants with increased upper-pole fullness and forward projection",
    "Teardrop / Anatomical Implants": "anatomical teardrop implants with a sloped upper pole and fuller lower pole",
    "Very Firm Augmented Projection": "very firm augmented projection with high upper-pole fullness and minimal natural drop",
}
BUTTOCKS = ["Unspecified", "Small", "Average", "Rounded", "Full", "Wide", "Athletic", "Prominent"]
DEFAULT_CLOTHING = [
    "Simple Fitted T-Shirt", "Opaque Fitted Tank Top", "Casual Jeans and T-Shirt",
    "Fitted Athletic Outfit", "Simple Dress", "Business Casual", "Swimwear",
    "Clinical Unclothed Documentation", "Custom",
]
JEWELRY_LEVELS = ["None", "Minimal", "Everyday", "Statement", "Custom"]
MARK_STATUSES = ["None", "One", "Multiple"]

SHOT_TYPES = ["Face Close-Up", "Head and Shoulders", "Chest-Up", "Waist-Up Midshot", "Three-Quarter Body", "Full Body", "Body Close-Up"]
SHOT_PROMPTS = {
    "Face Close-Up": "close-up face portrait framed from slightly above the complete head to the upper shoulders, face occupying most of the image",
    "Head and Shoulders": "head-and-shoulders portrait with full head, hair, neck, shoulders, and upper chest visible",
    "Chest-Up": "chest-up portrait framed from slightly above the complete head to below the chest, both shoulders and upper arms visible",
    "Waist-Up Midshot": "true waist-up midshot framed from slightly above the complete head to the navel or lower mid-abdomen, full head, both shoulders, arms, torso, natural waist, and mid-abdomen visible",
    "Three-Quarter Body": "three-quarter-body photograph framed from slightly above the complete head to below the knees, arms and legs clearly visible",
    "Full Body": "full-body photograph with the entire subject visible from head to feet and balanced space around the body",
    "Body Close-Up": "focused body-documentation close-up of the selected region with that region fully visible and centered",
}
CAMERA_VIEWS = ["Front View", "Three-Quarter Left", "Three-Quarter Right", "Left Profile", "Right Profile", "Rear Three-Quarter Left", "Rear Three-Quarter Right", "Back View"]
CAMERA_PROMPTS = {
    "Front View": "front-facing camera view, camera centered",
    "Three-Quarter Left": "three-quarter-left camera view, body and face turned approximately 45 degrees left",
    "Three-Quarter Right": "three-quarter-right camera view, body and face turned approximately 45 degrees right",
    "Left Profile": "true left-profile camera view",
    "Right Profile": "true right-profile camera view",
    "Rear Three-Quarter Left": "rear three-quarter-left camera view",
    "Rear Three-Quarter Right": "rear three-quarter-right camera view",
    "Back View": "direct back-facing camera view",
}
POSES = ["Neutral Standing", "Relaxed Standing", "Seated", "Leaning", "Walking", "Arms Relaxed", "Arms Loosely Crossed", "One Hand at Waist", "Custom"]
EXPRESSIONS = ["Neutral", "Natural Closed-Mouth Smile", "Genuine Smile", "Serious", "Focused", "Thoughtful", "Custom"]
BODY_REGIONS = ["Upper Torso", "Chest and Ribcage", "Abdomen and Waist", "Upper Back and Shoulders", "Lower Back and Waist", "Hips Front", "Hips Rear", "Left Side Torso", "Right Side Torso", "Custom"]
STAGES = ["Krea Identity Anchor", "Qwen Face Documentation", "Qwen Upper-Body Anchor", "Qwen Anatomy Documentation", "Qwen Clothing Edit", "Qwen Body Close-Up", "Krea Mini-LoRA Expansion"]
CLOTHING_MODES = ["Profile Default", "Exact Outfit Override", "Clinical Unclothed", "Preserve Reference Clothing"]
BACKGROUNDS = ["Plain Neutral", "Simple Indoor", "Simple Outdoor", "Clinical Neutral", "Natural Home", "Gym", "Custom"]
LIGHTING = ["Soft Natural Daylight", "Even Window Light", "Clinical Even Light", "Warm Indoor Light", "Overcast Outdoor Light", "Custom"]
PHOTO_STYLES = ["Authentic Consumer Camera", "Personal Cellphone Photo", "Identity Documentation", "Clinical Documentation", "Standard Camera Photo"]


def _heritage_prompt(heritage: str, custom: str) -> str:
    if heritage == "Unspecified": return ""
    if heritage == "Custom": return custom.strip()
    return f"{heritage.lower()} heritage"


def _hair_value(value: str, custom: str, label: str) -> str:
    if value == "Custom": return custom.strip()
    return f"{value.lower()} {label}" if value else ""


def _bust_prompt(gender: str, size: str, shape: str, position: str, firmness: str, augmentation: str) -> str:
    if gender != "Adult Female": return ""
    return _join(
        BUST_SIZE_PROMPTS.get(size, ""),
        BUST_SHAPE_PROMPTS.get(shape, ""),
        BUST_POSITION_PROMPTS.get(position, ""),
        BUST_FIRMNESS_PROMPTS.get(firmness, ""),
        BUST_AUGMENTATION_PROMPTS.get(augmentation, ""),
    )


def _split_lines(text: str) -> list[str]:
    values = []
    for block in re.split(r"[\r\n;]+", text or ""):
        cleaned = re.sub(r"^\s*(?:[-*•]+|\d+[.)])\s*", "", block).strip(" ,.;")
        if cleaned: values.append(cleaned)
    return values


def _marks_prompt(kind: str, status: str, description: str) -> tuple[str, list[str], str]:
    if status == "None": return "", [], ""
    entries = _split_lines(description)
    warnings = []
    if not entries:
        warnings.append(f"{kind} status is enabled but no descriptor was provided.")
    if status == "One" and len(entries) > 1:
        warnings.append(f"One {kind.lower()} is selected but multiple lines were supplied.")
    if status == "Multiple" and len(entries) < 2:
        warnings.append(f"Multiple {kind.lower()}s are selected but fewer than two lines were supplied.")
    if not entries: return "", [], " ".join(warnings)
    if len(entries) == 1:
        prompt = f"one permanent identity {kind.lower()} with exact placement: {entries[0]}"
    else:
        numbered = "; ".join(f"{kind.lower()} {i}: {entry}" for i, entry in enumerate(entries, 1))
        prompt = f"{len(entries)} separate permanent identity {kind.lower()}s with exact placements: {numbered}"
    return prompt, entries, " ".join(warnings)


def _visible_marks(entries: list[str], shot_type: str) -> str:
    if not entries: return ""
    if shot_type in {"Face Close-Up", "Head and Shoulders", "Chest-Up", "Waist-Up Midshot", "Three-Quarter Body", "Full Body"}:
        return "; ".join(entries)
    return "; ".join(entries)


class CharacterBlueprintCreator:
    CATEGORY = "character creation/core"
    FUNCTION = "build_blueprint"
    DESCRIPTION = "Creates a reusable adult character blueprint with separate face, body, bust, markings, and clothing prompts."

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "CHARACTER_BLUEPRINT", "STRING")
    RETURN_NAMES = ("face_identity", "upper_body_identity", "lower_body_identity", "bust_prompt", "marks_prompt", "default_clothing_prompt", "full_profile_prompt", "character_id", "character_blueprint", "warnings")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gender": (GENDERS, {"default": "Adult Female"}),
                "age_range": (AGE_RANGES, {"default": "25–34"}),
                "heritage": (HERITAGES, {"default": "Unspecified"}),
                "skin_tone": (SKIN_TONES, {"default": "Light"}),
                "complexion": (COMPLEXIONS, {"default": "Natural Skin Texture"}),
                "face_shape": (FACE_SHAPES, {"default": "Oval"}),
                "jaw_shape": (JAW_SHAPES, {"default": "Defined"}),
                "chin_shape": (CHIN_SHAPES, {"default": "Rounded"}),
                "eye_color": (EYE_COLORS, {"default": "Hazel"}),
                "eye_shape": (EYE_SHAPES, {"default": "Almond"}),
                "eyebrow_shape": (EYEBROWS, {"default": "Soft Arch"}),
                "nose_shape": (NOSES, {"default": "Straight"}),
                "lip_shape": (LIPS, {"default": "Balanced Medium"}),
                "hair_color": (HAIR_COLORS, {"default": "Medium Brown"}),
                "hair_length": (HAIR_LENGTHS, {"default": "Shoulder-Length"}),
                "hair_texture": (HAIR_TEXTURES, {"default": "Slightly Wavy"}),
                "hair_style": (HAIR_STYLES, {"default": "Loose Natural"}),
                "height": (HEIGHTS, {"default": "Average"}),
                "body_type": (BODY_TYPES, {"default": "Average"}),
                "bust_size": (BUST_SIZES, {"default": "Medium"}),
                "bust_shape": (BUST_SHAPES, {"default": "Teardrop"}),
                "bust_position": (BUST_POSITIONS, {"default": "Natural Average-Set"}),
                "bust_firmness": (BUST_FIRMNESS, {"default": "Balanced Natural"}),
                "bust_augmentation": (BUST_AUGMENTATION, {"default": "Natural / Unaugmented"}),
                "buttocks": (BUTTOCKS, {"default": "Average"}),
                "default_clothing": (DEFAULT_CLOTHING, {"default": "Simple Fitted T-Shirt"}),
                "jewelry_level": (JEWELRY_LEVELS, {"default": "Minimal"}),
                "tattoo_status": (MARK_STATUSES, {"default": "None"}),
                "piercing_status": (MARK_STATUSES, {"default": "None"}),
            },
            "optional": {
                "custom_heritage": ("STRING", {"default": "", "multiline": False}),
                "custom_hair_color": ("STRING", {"default": "", "multiline": False}),
                "custom_hair_length": ("STRING", {"default": "", "multiline": False}),
                "custom_hair_texture": ("STRING", {"default": "", "multiline": False}),
                "custom_hair_style": ("STRING", {"default": "", "multiline": False}),
                "exact_default_clothing": ("STRING", {"default": "", "multiline": True}),
                "jewelry_description": ("STRING", {"default": "", "multiline": True}),
                "tattoo_descriptors": ("STRING", {"default": "", "multiline": True, "placeholder": "One tattoo per line, including exact location"}),
                "piercing_descriptors": ("STRING", {"default": "", "multiline": True, "placeholder": "One piercing per line, including exact location and jewelry"}),
                "lower_body_notes": ("STRING", {"default": "", "multiline": True}),
                "custom_identity_notes": ("STRING", {"default": "", "multiline": True}),
            },
        }

    def build_blueprint(self, gender, age_range, heritage, skin_tone, complexion, face_shape, jaw_shape, chin_shape, eye_color, eye_shape, eyebrow_shape, nose_shape, lip_shape, hair_color, hair_length, hair_texture, hair_style, height, body_type, bust_size, bust_shape, bust_position, bust_firmness, bust_augmentation, buttocks, default_clothing, jewelry_level, tattoo_status, piercing_status, custom_heritage="", custom_hair_color="", custom_hair_length="", custom_hair_texture="", custom_hair_style="", exact_default_clothing="", jewelry_description="", tattoo_descriptors="", piercing_descriptors="", lower_body_notes="", custom_identity_notes=""):
        heritage_prompt = _heritage_prompt(heritage, custom_heritage)
        face_identity = _join(
            "adult subject", gender.lower(), f"age range {age_range}", heritage_prompt,
            f"{skin_tone.lower()} skin tone" if skin_tone != "Custom / Unspecified" else "",
            complexion.lower() if complexion != "Unspecified" else "",
            f"{face_shape.lower()} face", f"{jaw_shape.lower()} jaw", f"{chin_shape.lower()} chin",
            f"{eye_color.lower()} eyes" if eye_color != "Custom / Unspecified" else "",
            f"{eye_shape.lower()} eye shape", f"{eyebrow_shape.lower()} eyebrows",
            f"{nose_shape.lower()} nose", f"{lip_shape.lower()} lips",
            _hair_value(hair_color, custom_hair_color, "hair"),
            _hair_value(hair_length, custom_hair_length, "hair length"),
            _hair_value(hair_texture, custom_hair_texture, "hair texture"),
            _hair_value(hair_style, custom_hair_style, "hairstyle"),
            custom_identity_notes,
        )
        bust_prompt = _bust_prompt(gender, bust_size, bust_shape, bust_position, bust_firmness, bust_augmentation)
        upper_body_identity = _join(
            f"{height.lower()} height" if height != "Unspecified" else "",
            f"{body_type.lower()} body type" if body_type != "Custom / Unspecified" else "",
            bust_prompt,
        )
        lower_body_identity = _join(
            f"{buttocks.lower()} buttocks" if buttocks != "Unspecified" else "",
            lower_body_notes,
        )
        tattoo_prompt, tattoo_entries, tattoo_warning = _marks_prompt("Tattoo", tattoo_status, tattoo_descriptors)
        piercing_prompt, piercing_entries, piercing_warning = _marks_prompt("Piercing", piercing_status, piercing_descriptors)
        marks_prompt = _join(tattoo_prompt, piercing_prompt)
        if exact_default_clothing.strip():
            clothing_prompt = f"wearing {exact_default_clothing.strip()}"
        elif default_clothing == "Clinical Unclothed Documentation":
            clothing_prompt = "unclothed adult subject in neutral clinical anatomy documentation"
        elif default_clothing == "Custom":
            clothing_prompt = ""
        else:
            clothing_prompt = f"wearing {default_clothing.lower()}"
        jewelry_prompt = "" if jewelry_level == "None" else _join(f"{jewelry_level.lower()} jewelry", jewelry_description)
        default_clothing_prompt = _join(clothing_prompt, jewelry_prompt)
        full_profile_prompt = _join(face_identity, marks_prompt, upper_body_identity, lower_body_identity, default_clothing_prompt)
        base_id = _join(gender, age_range, heritage, face_shape, hair_color, body_type, bust_size)
        character_id = _slug(base_id) + "_" + hashlib.sha1(full_profile_prompt.encode("utf-8")).hexdigest()[:8]
        warnings = " ".join(x for x in [tattoo_warning, piercing_warning] if x)
        if bust_position == "High and Tight" and bust_firmness in {"Soft", "Very Soft / Natural Movement"}:
            warnings = _join(warnings, "High and Tight conflicts with the selected soft-tissue setting.")
        blueprint = {
            "schema": "CHARACTER_BLUEPRINT",
            "schema_version": 1,
            "character_id": character_id,
            "gender": gender,
            "age_range": age_range,
            "heritage": heritage,
            "heritage_prompt": heritage_prompt,
            "face_identity": face_identity,
            "upper_body_identity": upper_body_identity,
            "lower_body_identity": lower_body_identity,
            "bust_prompt": bust_prompt,
            "marks_prompt": marks_prompt,
            "tattoo_entries": tattoo_entries,
            "piercing_entries": piercing_entries,
            "default_clothing_prompt": default_clothing_prompt,
            "full_profile_prompt": full_profile_prompt,
            "warnings": warnings,
        }
        return (face_identity, upper_body_identity, lower_body_identity, bust_prompt, marks_prompt, default_clothing_prompt, full_profile_prompt, character_id, blueprint, warnings)


class CharacterShotPlanner:
    CATEGORY = "character creation/core"
    FUNCTION = "plan_shot"
    DESCRIPTION = "Builds stage-specific Krea and Qwen prompts from a Character Blueprint without sending irrelevant anatomy to face-only shots."

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "INT", "INT", "STRING", "STRING")
    RETURN_NAMES = ("krea_prompt", "qwen_prompt", "shot_prompt", "clothing_prompt", "marks_prompt", "reference_required", "shot_id", "recommended_width", "recommended_height", "profile_character_id", "planner_notes")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "stage": (STAGES, {"default": "Krea Identity Anchor"}),
                "shot_type": (SHOT_TYPES, {"default": "Face Close-Up"}),
                "camera_view": (CAMERA_VIEWS, {"default": "Front View"}),
                "pose": (POSES, {"default": "Neutral Standing"}),
                "expression": (EXPRESSIONS, {"default": "Neutral"}),
                "clothing_mode": (CLOTHING_MODES, {"default": "Profile Default"}),
                "body_region": (BODY_REGIONS, {"default": "Upper Torso"}),
                "background": (BACKGROUNDS, {"default": "Plain Neutral"}),
                "lighting": (LIGHTING, {"default": "Soft Natural Daylight"}),
                "photo_style": (PHOTO_STYLES, {"default": "Authentic Consumer Camera"}),
            },
            "optional": {
                "character_blueprint": ("CHARACTER_BLUEPRINT",),
                "exact_outfit": ("STRING", {"default": "", "multiline": True}),
                "custom_pose": ("STRING", {"default": "", "multiline": True}),
                "custom_expression": ("STRING", {"default": "", "multiline": False}),
                "custom_body_region": ("STRING", {"default": "", "multiline": True}),
                "custom_background": ("STRING", {"default": "", "multiline": True}),
                "custom_lighting": ("STRING", {"default": "", "multiline": True}),
                "trigger_word": ("STRING", {"default": "", "multiline": False}),
                "custom_suffix": ("STRING", {"default": "", "multiline": True}),
            },
        }

    def plan_shot(self, stage, shot_type, camera_view, pose, expression, clothing_mode, body_region, background, lighting, photo_style, character_blueprint=None, exact_outfit="", custom_pose="", custom_expression="", custom_body_region="", custom_background="", custom_lighting="", trigger_word="", custom_suffix=""):
        profile = character_blueprint if isinstance(character_blueprint, dict) else {}
        face = profile.get("face_identity", "adult subject")
        upper = profile.get("upper_body_identity", "")
        lower = profile.get("lower_body_identity", "")
        marks = profile.get("marks_prompt", "")
        default_clothing = profile.get("default_clothing_prompt", "")
        full_profile = profile.get("full_profile_prompt", _join(face, upper, lower, marks, default_clothing))
        character_id = profile.get("character_id", "character")

        shot_prompt = _join(SHOT_PROMPTS[shot_type], CAMERA_PROMPTS[camera_view])
        if shot_type == "Body Close-Up":
            region = custom_body_region.strip() if body_region == "Custom" and custom_body_region.strip() else body_region
            shot_prompt = _join(shot_prompt, f"focused on {region.lower()}")
        pose_prompt = custom_pose.strip() if pose == "Custom" and custom_pose.strip() else pose.lower()
        expression_prompt = custom_expression.strip() if expression == "Custom" and custom_expression.strip() else expression.lower() + " expression"
        background_prompt = custom_background.strip() if background == "Custom" and custom_background.strip() else background.lower() + " background"
        lighting_prompt = custom_lighting.strip() if lighting == "Custom" and custom_lighting.strip() else lighting.lower()
        style_prompt = photo_style.lower()

        if clothing_mode == "Exact Outfit Override":
            clothing_prompt = f"wearing {exact_outfit.strip()}" if exact_outfit.strip() else "wearing the exact requested outfit"
        elif clothing_mode == "Clinical Unclothed":
            clothing_prompt = "unclothed adult subject in neutral clinical anatomy documentation"
        elif clothing_mode == "Preserve Reference Clothing":
            clothing_prompt = "preserve the clothing already visible in Image 1"
        else:
            clothing_prompt = default_clothing

        face_only = shot_type in {"Face Close-Up", "Head and Shoulders"}
        upper_visible = shot_type in {"Chest-Up", "Waist-Up Midshot", "Three-Quarter Body", "Full Body", "Body Close-Up"}
        lower_visible = shot_type in {"Three-Quarter Body", "Full Body", "Body Close-Up"}

        krea_identity = _join(face, marks, "" if face_only else upper, lower if lower_visible else "", clothing_prompt)
        krea_prompt = _join(trigger_word, shot_prompt, pose_prompt, expression_prompt, krea_identity, background_prompt, lighting_prompt, style_prompt, custom_suffix)

        if stage == "Krea Identity Anchor":
            reference = "None — text-to-image"
            qwen_prompt = ""
            planner_notes = "Krea receives face, hair, visible markings, and only the body traits relevant to the selected crop."
        elif stage == "Qwen Face Documentation":
            reference = "Portrait Anchor"
            qwen_prompt = _join(
                "Edit Image 1 into a realistic photograph of the same adult person",
                "preserve the exact recognizable face, hair, skin characteristics, and permanent facial markings from Image 1",
                shot_prompt, pose_prompt, expression_prompt, face, marks,
                background_prompt, lighting_prompt, style_prompt,
                "keep natural skin texture, realistic moist eyes, ordinary camera sharpness, and believable hair strands",
                custom_suffix,
            )
            planner_notes = "Uses only face, hair, expression, camera, and permanent markings."
        elif stage == "Qwen Upper-Body Anchor":
            reference = "Portrait Anchor"
            qwen_prompt = _join(
                "Edit Image 1 into a realistic waist-up photograph of the same adult person",
                "preserve the exact recognizable face and hair from Image 1",
                shot_prompt, pose_prompt, expression_prompt, face, marks, upper, clothing_prompt,
                background_prompt, lighting_prompt, style_prompt,
                "establish consistent shoulders, chest, torso, arms, and natural waist while preserving identity",
                custom_suffix,
            )
            planner_notes = "Introduces upper-body and bust traits; lower-body traits remain excluded."
        elif stage == "Qwen Anatomy Documentation":
            reference = "Portrait or Anatomy Anchor"
            qwen_prompt = _join(
                "Edit Image 1 into neutral adult clinical anatomy documentation of the same person",
                "preserve exact face, hair, body proportions, tattoos, and piercings",
                shot_prompt, pose_prompt, face, marks, upper, lower, clothing_prompt,
                background_prompt, lighting_prompt, "clinical documentation photography", custom_suffix,
            )
            planner_notes = "Use Clinical Unclothed clothing mode for anatomy documentation."
        elif stage == "Qwen Clothing Edit":
            reference = "Anatomy or Clothed Anchor"
            qwen_prompt = _join(
                "Edit Image 1 into a realistic wardrobe photograph of the same adult person",
                "preserve the exact face, hair, body shape, chest proportions, waist, tattoos, and piercings from Image 1",
                shot_prompt, pose_prompt, expression_prompt,
                f"replace the current clothing state with {clothing_prompt}",
                "the requested garment is fully worn with realistic fabric, seams, folds, and fit",
                background_prompt, lighting_prompt, style_prompt, custom_suffix,
            )
            planner_notes = "Exact Outfit Override is recommended for wardrobe tests."
        elif stage == "Qwen Body Close-Up":
            reference = "Anatomy Anchor"
            qwen_prompt = _join(
                "Edit Image 1 into focused adult body-documentation photography of the same person",
                "preserve exact body proportions, skin characteristics, tattoos, and piercings",
                shot_prompt, pose_prompt, upper if upper_visible else "", lower if lower_visible else "", marks, clothing_prompt,
                background_prompt, lighting_prompt, "clinical documentation photography", custom_suffix,
            )
            planner_notes = "Select Body Close-Up and the exact body region."
        else:
            reference = "Mini LoRA loaded in Krea model lane"
            qwen_prompt = ""
            krea_prompt = _join(trigger_word, shot_prompt, pose_prompt, expression_prompt, full_profile, clothing_prompt, background_prompt, lighting_prompt, style_prompt, custom_suffix)
            planner_notes = "Krea expansion uses the complete profile because identity is supplied by the mini LoRA."

        if shot_type == "Face Close-Up": width, height = 1024, 1024
        elif shot_type in {"Head and Shoulders", "Chest-Up", "Waist-Up Midshot", "Body Close-Up"}: width, height = 1024, 1280
        else: width, height = 1024, 1536
        shot_id = _slug(_join(character_id, stage, shot_type, camera_view, pose))
        return (krea_prompt, qwen_prompt, shot_prompt, clothing_prompt, marks, reference, shot_id, width, height, character_id, planner_notes)
