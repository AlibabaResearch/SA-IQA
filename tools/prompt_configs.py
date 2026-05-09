SUBSET_MAP = {
    "distortion": "2k",
    "harmony": "7k",
    "layout": "6k",
    "lighting": "3k",
}

PROMPTS = {
    1: {
        "distortion": "<image>Please evaluate the spatial aesthetic distortion quality level of this image.",
        "harmony": "<image>Please evaluate the spatial aesthetic harmony quality level of this image.",
        "layout": "<image>Please evaluate the spatial aesthetic layout quality level of this image.",
        "lighting": "<image>Please evaluate the spatial aesthetic lighting quality level of this image.",
    },
    2: {
        "distortion": "<image><distortion>Please evaluate the spatial aesthetic distortion quality level of this image.",
        "harmony": "<image><harmony>Please evaluate the spatial aesthetic harmony quality level of this image.",
        "layout": "<image><layout>Please evaluate the spatial aesthetic layout quality level of this image.",
        "lighting": "<image><lighting>Please evaluate the spatial aesthetic lighting quality level of this image.",
    },
    3: {
        "distortion": (
            "<image><distortion>Please evaluate the spatial aesthetic distortion quality level of this image. "
            "The distortion dimension describes the degree of distortion in shapes or the fidelity of background "
            "details. Assess how the distortion impacts the perceived realism and visual quality of the image."
        ),
        "harmony": (
            "<image><harmony>Please evaluate the spatial aesthetic harmony quality level of this image. "
            "The harmony dimension emphasizes stylistic consistency, color matching, and overall visual coordination. "
            "Consider how well the elements come together to create a unified and pleasing appearance."
        ),
        "layout": (
            "<image><layout>Please evaluate the spatial aesthetic layout quality level of this image. "
            "The layout dimension describes the spatial distribution and positional relationships of major elements "
            "within a composition. Assess how the layout contributes to the overall organization, structure, and "
            "balance of the image."
        ),
        "lighting": (
            "<image><lighting>Please evaluate the spatial aesthetic lighting quality level of this image. "
            "The lighting dimension focuses on the interaction between light and shadow, including the quality of "
            "lighting effects and the sense of three-dimensionality. Assess how lighting enhances or affects the "
            "depth and overall atmosphere of an image."
        ),
    },
    4: {
        "distortion": (
            "<image><distortion>Please evaluate the spatial aesthetic distortion quality level of this image. "
            "The distortion dimension assesses whether soft furnishings (e.g., cabinets, carpets) or fixed "
            "structures (e.g., floors, walls) appear deformed or misaligned. Additionally, evaluate the realism "
            "and material accuracy of textures, and judge whether any distortion negatively impacts the overall "
            "aesthetic quality of the image."
        ),
        "harmony": (
            "<image><harmony>Please evaluate the spatial aesthetic harmony quality level of this image. "
            "The harmony dimension focuses on stylistic consistency, color coordination, and overall visual cohesion. "
            "Examine how well the combination of elements creates a balanced and visually pleasant composition, "
            "avoiding clashes or imbalances in style and color."
        ),
        "layout": (
            "<image><layout>Please evaluate the spatial aesthetic layout quality level of this image. "
            "The layout dimension describes the spatial distribution, positional relationships, and quantity of major "
            "elements within the space. Consider how the layout supports the overall visual order, maintains balance, "
            "and enhances the functional aesthetics of the image."
        ),
        "lighting": (
            "<image><lighting>Please evaluate the spatial aesthetic lighting quality level of this image. "
            "The lighting dimension examines the quality of light effects, shadow interactions, and the realism of "
            "light sources. Assess how well lighting contributes to the overall depth, mood, and authenticity of the "
            "image, emphasizing both natural and artificial lighting scenarios."
        ),
    },
}

PROMPT_VERSIONS = sorted(PROMPTS)
