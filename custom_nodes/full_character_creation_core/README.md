# Full Character Creation Core v1.2

Nodes:

- Character Blueprint Creator v1.2
- Character Shot Planner v1.2
- FCC Qwen Dataset Queue v1.0

## v1.2 additions

- Optional `character_blueprint_json` output.
- Structured piercing controls with septum-specific placement language.
- Expanded expression selector, including `Ahegao (Stylized Adult)` as an optional non-default expression.
- One-click Qwen Image Edit dataset queue using an approved headshot as Image 1.
- Bootstrap plans: 24, 40, or 60 images.
- Post-LoRA anatomy/action plans: 40, 60, or 120 images.
- List outputs for prompts, seeds, shot IDs, categories, filename prefixes, and dimensions.

The queue node does not create a second Qwen pipeline. Connect its list outputs to one reusable Qwen Image Edit lane. ComfyUI maps the list items through the downstream graph.
