import { app } from "../../../scripts/app.js";

const VARIANTS_BY_TYPE = {
  "Extreme Close-Up": [
    "Both Eyes Centered",
    "Left Eye",
    "Right Eye",
    "Eyebrows",
    "Forehead",
    "Nose",
    "Mouth and Lips",
    "Teeth and Smile",
    "Left Ear",
    "Right Ear",
    "Jawline",
    "Hairline",
    "Neck Front",
    "Neck Side",
	"Both Breasts",
	"Breast Left",
	"Breast Right"
	"Nipple and Areola",
	"Ass",
	"Pussy",
	"Pubis Mons"
  ],
  "Close-Up Portrait": [
    "Front Neutral",
    "Front Smiling",
    "Front Serious",
    "45 Degree Left",
    "45 Degree Right",
    "Profile Left",
    "Profile Right",
    "Back View",
    "Back 45 Degree Left",
    "Back 45 Degree Right",
    "Looking Up",
    "Looking Down",
    "Looking Left",
    "Looking Right",
    "Over Left Shoulder",
    "Over Right Shoulder"
  ],
  "Midshot": [
    "Standing Neutral",
    "Hands on Hips",
    "Arms Crossed",
    "Hands Relaxed",
    "Leaning Against Wall",
    "Looking Over Shoulder",
    "Walking Forward",
    "Seated on Chair",
    "Seated on Couch",
    "Holding Coffee Mug",
    "Holding Phone",
    "Reading a Book",
    "Working on Laptop",
    "Casual Laugh",
    "One Hand in Pocket",
    "Adjusting Hair"
  ],
  "Full Body": [
    "Standing Front",
    "Standing Back",
    "Standing Left Side",
    "Standing Right Side",
    "Walking Toward Camera",
    "Walking Away",
    "Seated on Chair",
    "Seated on Floor",
    "Cross-Legged",
    "Kneeling",
    "Leaning Against Wall",
    "Hands in Pockets",
    "One Leg Forward",
    "Arms Raised",
    "Turning Around",
    "Relaxed Casual Stance"
  ],
  "Body Anatomy / Part Focus": [
    "Both Hands Front",
    "Both Hands Back",
    "Left Hand",
    "Right Hand",
    "Fingers",
    "Both Feet Front",
    "Both Feet Side",
    "Left Foot",
    "Right Foot",
    "Eyes",
    "Mouth and Lips",
    "Teeth",
    "Hair",
    "Neck",
    "Shoulders",
    "Upper Chest / Bust",
    "Back",
    "Waist",
    "Hips",
    "Buttocks",
    "Thighs",
    "Knees",
    "Calves",
    "Arms",
    "Elbows",
	"Forearm",
	"Upperarm",
	"Ear",
	"Pussy"
	"Trimmed female pubic hair"
	
  ]
};

function findWidget(node, name) {
    return node.widgets?.find((widget) => widget.name === name);
}

function updateCombo(widget, values) {
    if (!widget || !Array.isArray(values) || values.length === 0) return;

    widget.options = widget.options || {};
    widget.options.values = [...values];

    if (!values.includes(widget.value)) {
        widget.value = values[0];
        widget.callback?.(widget.value);
    }
}

function setWidgetVisible(node, widget, visible) {
    if (!widget) return;

    if (!widget.__datasetShotPlannerOriginalType) {
        widget.__datasetShotPlannerOriginalType = widget.type;
        widget.__datasetShotPlannerOriginalComputeSize = widget.computeSize;
    }

    if (visible) {
        widget.type = widget.__datasetShotPlannerOriginalType;
        widget.computeSize = widget.__datasetShotPlannerOriginalComputeSize;
    } else {
        widget.type = "hidden";
        widget.computeSize = () => [0, -4];
    }

    node.setSize?.([node.size[0], node.computeSize()[1]]);
    node.setDirtyCanvas?.(true, true);
}

function updateChestVisibility(node) {
    const gender = findWidget(node, "gender");
    const chest = findWidget(node, "female_chest_size");
    if (!gender || !chest) return;
    setWidgetVisible(node, chest, gender.value === "Female");
}

app.registerExtension({
    name: "dataset_shot_planner.dynamic_variants",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "DatasetShotPlanner") return;

        const originalOnNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = function () {
            const result = originalOnNodeCreated?.apply(this, arguments);
            const shotType = findWidget(this, "shot_type");
            const variant = findWidget(this, "shot_variant");
            const gender = findWidget(this, "gender");

            if (!shotType || !variant) return result;

            const refresh = () => {
                updateCombo(variant, VARIANTS_BY_TYPE[shotType.value] || []);
                this.setDirtyCanvas?.(true, true);
            };

            const oldCallback = shotType.callback;
            shotType.callback = (value) => {
                oldCallback?.call(shotType, value);
                refresh();
            };

            if (gender) {
                const oldGenderCallback = gender.callback;
                gender.callback = (value) => {
                    oldGenderCallback?.call(gender, value);
                    updateChestVisibility(this);
                };
            }

            requestAnimationFrame(() => {
                refresh();
                updateChestVisibility(this);
            });
            return result;
        };
    },
});
