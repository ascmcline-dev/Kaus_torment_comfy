class RGBImageMaskPass:
    CATEGORY = "utils/image"
    FUNCTION = "run"

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
            }
        }

    def run(self, image, mask):
        if image.ndim != 4:
            raise ValueError(f"Expected IMAGE [B,H,W,C], got {tuple(image.shape)}")

        channels = image.shape[-1]

        if channels >= 4:
            rgb = image[:, :, :, :3]
        elif channels == 3:
            rgb = image
        elif channels == 1:
            rgb = image.repeat(1, 1, 1, 3)
        else:
            raise ValueError(f"Unsupported channel count: {channels}")

        return (rgb, mask)