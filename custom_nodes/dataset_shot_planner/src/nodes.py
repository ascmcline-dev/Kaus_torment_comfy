
from __future__ import annotations

import hashlib
import random
import re
from typing import List

from .prompt_data import (
    SHOT_VARIANTS,
    ALL_VARIANTS,
    SHOT_BASE,
    PHOTO_STYLES,
    EXPRESSIONS,
    LIGHTING,
    BACKGROUNDS,
    OUTFITS,
    NEGATIVE_PRESETS,
    GENDERS,
    BODY_TYPES,
    FEMALE_CHEST_SIZES,
)

SHOT_TYPES = list(SHOT_VARIANTS.keys())
PHOTO_STYLE_NAMES = list(PHOTO_STYLES.keys())
EXPRESSION_NAMES = list(EXPRESSIONS.keys())
LIGHTING_NAMES = list(LIGHTING.keys())
BACKGROUND_NAMES = list(BACKGROUNDS.keys())
OUTFIT_NAMES = list(OUTFITS.keys())
NEGATIVE_NAMES = list(NEGATIVE_PRESETS.keys())
GENDER_NAMES = list(GENDERS.keys())
BODY_TYPE_NAMES = list(BODY_TYPES.keys())


def _clean_join(parts: List[str]) -> str:
    return ", ".join(part.strip(" ,") for part in parts if part and part.strip(" ,"))


def _slug(text: str) -> str:
    value = text.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def _variant_to_prompt(variant: str) -> str:
    direct = {
        "Both Eyes Centered": "camera centered directly on both eyes, both eyes fully visible, symmetrical eye-level view",
        "Left Eye": "focus on the left eye and surrounding eyelid and eyebrow anatomy",
        "Right Eye": "focus on the right eye and surrounding eyelid and eyebrow anatomy",
        "Eyebrows": "focus on both eyebrows and the brow ridge",
        "Forehead": "focus on the forehead and hairline transition",
        "Nose": "focus on the nose from a centered frontal view",
        "Mouth and Lips": "focus on the mouth and lips in a relaxed natural position",
        "Teeth and Smile": "focus on a natural smile with teeth clearly visible",
        "Teeth": "natural smile with teeth clearly visible",
        "Left Ear": "focus on the left ear from a clean side angle",
        "Right Ear": "focus on the right ear from a clean side angle",
        "Jawline": "focus on the jawline and chin contour",
        "Hairline": "focus on the front hairline and temple area",
        "Neck Front": "focus on the front of the neck and collarbone area",
        "Neck Side": "focus on the side of the neck from a three-quarter angle",
        "Front Neutral": "front-facing view, camera centered, neutral expression",
        "Front Smiling": "front-facing view, camera centered, natural relaxed smile",
        "Front Serious": "front-facing view, camera centered, calm serious expression",
        "45 Degree Left": "head turned approximately 45 degrees to the subject's left, both eyes still visible",
        "45 Degree Right": "head turned approximately 45 degrees to the subject's right, both eyes still visible",
        "Profile Left": "true left profile view, face turned 90 degrees",
        "Profile Right": "true right profile view, face turned 90 degrees",
        "Back View": "back of head and upper shoulders facing camera",
        "Back 45 Degree Left": "back three-quarter view turned approximately 45 degrees left",
        "Back 45 Degree Right": "back three-quarter view turned approximately 45 degrees right",
        "Looking Up": "chin raised slightly, looking upward while keeping facial structure visible",
        "Looking Down": "chin lowered slightly, looking downward while keeping facial structure visible",
        "Looking Left": "eyes and head directed to the left",
        "Looking Right": "eyes and head directed to the right",
        "Over Left Shoulder": "looking back over the left shoulder",
        "Over Right Shoulder": "looking back over the right shoulder",
        "Standing Neutral": "standing naturally with relaxed shoulders and balanced posture",
        "Hands on Hips": "standing with both hands resting naturally on the hips",
        "Arms Crossed": "standing with arms crossed comfortably across the torso",
        "Hands Relaxed": "hands relaxed naturally at the sides",
        "Leaning Against Wall": "leaning lightly against a wall in a relaxed pose",
        "Looking Over Shoulder": "torso angled away while looking back over one shoulder",
        "Walking Forward": "walking naturally toward the camera, mid-step",
        "Seated on Chair": "seated naturally on a chair with balanced posture",
        "Seated on Couch": "seated casually on a couch in a relaxed position",
        "Holding Coffee Mug": "holding a coffee mug naturally near the torso",
        "Holding Phone": "holding a phone casually in one hand",
        "Reading a Book": "holding and reading a book naturally",
        "Working on Laptop": "seated while naturally working on a laptop",
        "Casual Laugh": "caught during a relaxed natural laugh",
        "One Hand in Pocket": "standing with one hand casually placed in a pocket",
        "Adjusting Hair": "one hand naturally adjusting the hair",
        "Standing Front": "standing front-facing in a relaxed neutral stance",
        "Standing Back": "standing with the back facing the camera",
        "Standing Left Side": "standing in a true left-side view",
        "Standing Right Side": "standing in a true right-side view",
        "Walking Toward Camera": "walking naturally toward the camera, full body visible",
        "Walking Away": "walking naturally away from the camera, full body visible",
        "Seated on Floor": "seated naturally on the floor with the full body visible",
        "Cross-Legged": "seated cross-legged with balanced natural posture",
        "Kneeling": "kneeling naturally with full body and limbs visible",
        "Hands in Pockets": "standing casually with both hands in pockets",
        "One Leg Forward": "standing with one leg placed slightly forward",
        "Arms Raised": "standing with both arms raised naturally above shoulder level",
        "Turning Around": "captured while naturally turning around",
        "Relaxed Casual Stance": "relaxed casual full-body stance with natural weight distribution",
        "Both Hands Front": "both hands held forward with palms visible and fingers naturally separated",
        "Both Hands Back": "backs of both hands visible with fingers naturally separated",
        "Left Hand": "left hand isolated and clearly visible from a natural angle",
        "Right Hand": "right hand isolated and clearly visible from a natural angle",
        "Fingers": "close documentation of the fingers, joints, nails, and natural proportions",
        "Both Feet Front": "both feet visible from the front with natural spacing",
        "Both Feet Side": "both feet visible from a clean side angle",
        "Left Foot": "left foot isolated and clearly visible",
        "Right Foot": "right foot isolated and clearly visible",
        "Eyes": "both eyes and surrounding facial anatomy clearly visible",
        "Hair": "hair shape, texture, hairline, and overall arrangement clearly visible",
        "Neck": "neck and collarbone area clearly visible",
        "Shoulders": "both shoulders clearly visible with natural posture",
        "Upper Chest / Bust": "upper chest and bust area clearly framed in fitted, non-bulky clothing for anatomy and silhouette reference",
        "Back": "back anatomy and shoulder-blade area clearly visible",
        "Waist": "waistline and torso silhouette clearly visible",
        "Hips": "hips and pelvic silhouette clearly framed in fitted clothing",
        "Buttocks": "rear hip and buttocks silhouette clearly framed in fitted, non-bulky clothing for anatomy reference",
        "Thighs": "upper legs and thigh proportions clearly visible",
        "Knees": "both knees clearly visible from a natural angle",
        "Calves": "lower legs and calf proportions clearly visible",
        "Arms": "both arms clearly visible from shoulders to hands",
        "Elbows": "elbow joints and surrounding arm anatomy clearly visible",
    }
    return direct.get(variant, variant.replace("_", " ").lower())



def _subject_prompt(gender: str, body_type: str, female_chest_size: str) -> str:
    parts = [
        GENDERS.get(gender, ""),
        BODY_TYPES.get(body_type, ""),
    ]
    if gender == "Female" and female_chest_size != "Unspecified":
        parts.append(f"proportionate {female_chest_size} bust")
    return _clean_join(parts)

def _stable_choice(options: List[str], random_seed: int, salt: str) -> str:
    digest = hashlib.sha256(f"{random_seed}|{salt}".encode("utf-8")).digest()
    picker = random.Random(int.from_bytes(digest[:8], "big"))
    return picker.choice(options)


class DatasetShotPlanner:
    CATEGORY = "prompt/dataset"
    FUNCTION = "build_prompt"

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "combined_prompt",
        "shot_prompt",
        "style_prompt",
        "subject_prompt",
        "outfit_prompt",
        "negative_prompt",
        "shot_type",
        "shot_variant",
        "shot_id",
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shot_type": (SHOT_TYPES, {"default": "Close-Up Portrait"}),
                "shot_variant": (ALL_VARIANTS, {"default": "Front Neutral"}),
                "photography_style": (PHOTO_STYLE_NAMES, {"default": "Professional Photography Session"}),
                "gender": (GENDER_NAMES, {"default": "Unspecified"}),
                "body_type": (BODY_TYPE_NAMES, {"default": "Unspecified"}),
                "female_chest_size": (FEMALE_CHEST_SIZES, {"default": "Unspecified"}),
                "expression": (EXPRESSION_NAMES, {"default": "Neutral"}),
                "lighting": (LIGHTING_NAMES, {"default": "Use Style Default"}),
                "background": (BACKGROUND_NAMES, {"default": "Unspecified"}),
                "outfit_style": (OUTFIT_NAMES, {"default": "Varied Fitted Outfits"}),
                "negative_preset": (NEGATIVE_NAMES, {"default": "Standard Dataset"}),
                "randomize_variant": ("BOOLEAN", {"default": False}),
                "random_seed": ("INT", {"default": 1985, "min": 0, "max": 9223372036854775807, "step": 1}),
            },
            "optional": {
                "custom_prefix": ("STRING", {"default": "", "multiline": True}),
                "custom_suffix": ("STRING", {"default": "", "multiline": True}),
                "custom_negative": ("STRING", {"default": "", "multiline": True}),
            },
        }

    @classmethod
    def VALIDATE_INPUTS(cls, shot_type, shot_variant, **kwargs):
        if shot_type not in SHOT_VARIANTS:
            return f"Unknown shot_type: {shot_type}"
        if shot_variant not in ALL_VARIANTS:
            return f"Unknown shot_variant: {shot_variant}"
        return True

    def build_prompt(
        self,
        shot_type,
        shot_variant,
        photography_style,
        gender,
        body_type,
        female_chest_size,
        expression,
        lighting,
        background,
        outfit_style,
        negative_preset,
        randomize_variant,
        random_seed,
        custom_prefix="",
        custom_suffix="",
        custom_negative="",
    ):
        valid_variants = SHOT_VARIANTS.get(shot_type, SHOT_VARIANTS["Close-Up Portrait"])
        if randomize_variant:
            chosen_variant = _stable_choice(valid_variants, int(random_seed), shot_type)
        elif shot_variant in valid_variants:
            chosen_variant = shot_variant
        else:
            chosen_variant = valid_variants[0]

        shot_prompt = _clean_join([
            SHOT_BASE.get(shot_type, ""),
            _variant_to_prompt(chosen_variant),
            EXPRESSIONS.get(expression, ""),
            LIGHTING.get(lighting, ""),
            BACKGROUNDS.get(background, ""),
        ])
        style_prompt = PHOTO_STYLES.get(photography_style, "")
        subject_prompt = _subject_prompt(gender, body_type, female_chest_size)
        outfit_prompt = OUTFITS.get(outfit_style, "")
        combined_prompt = _clean_join([custom_prefix, subject_prompt, shot_prompt, style_prompt, outfit_prompt, custom_suffix])
        negative_prompt = _clean_join([NEGATIVE_PRESETS.get(negative_preset, ""), custom_negative])
        shot_id = "_".join([_slug(shot_type), _slug(chosen_variant), _slug(photography_style)])

        return (
            combined_prompt,
            shot_prompt,
            style_prompt,
            subject_prompt,
            outfit_prompt,
            negative_prompt,
            shot_type,
            chosen_variant,
            shot_id,
        )
