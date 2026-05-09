---
license: other
license_name: sa-iqa-model-non-commercial
license_link: LICENSE
language:
  - en
library_name: transformers
pipeline_tag: image-text-to-text
base_model: AIDC-AI/Ovis2.5-9B
datasets:
  - SA-BENCH
tags:
  - multimodal
  - vision-language
  - image-quality-assessment
  - aesthetics
  - spatial-aesthetics
  - interior-design
---

# SA-IQA Model

SA-IQA is a multimodal image quality assessment model released with **“Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics.”**

The released final checkpoint is **`sa-iqa-prompt4`**, a fine-tuned model based on **Ovis2.5-9B** for assessing interior-image spatial aesthetics.

## Hugging Face Upload Note

For a standard Hugging Face model repository, upload the contents of `sa-iqa-prompt4/` to the model repository root together with this `README.md` and `LICENSE`.

This release bundle also includes `Ovis2.5-9B/` for reproducibility, but Hugging Face model repositories are normally expected to expose one model configuration at the repository root. If you upload the whole `SA-IQA-model/` directory as-is, automatic model loading from the root may not work because model files are nested under `sa-iqa-prompt4/`.

## Model Details

### Model Description

- **Model type:** multimodal vision-language model for image quality assessment
- **Base model:** Ovis2.5-9B
- **Fine-tuned checkpoint:** sa-iqa-prompt4
- **Input:** image plus a dimension-specific text prompt
- **Output:** textual quality label and token log-probabilities used to compute a continuous score
- **Dimensions:** distortion, harmony, layout, lighting

### Intended Use

SA-IQA is intended for non-commercial research and evaluation, including:

- spatial aesthetic assessment of interior images
- image quality benchmarking on SA-BENCH
- reward-model research for image generation and best-of-N selection
- comparison of prompt variants for spatial aesthetic assessment

### Out-of-Scope Use

The model is not intended for:

- commercial deployment without prior permission
- universal aesthetic judgment outside the interior-scene domain
- safety-critical or legally binding decision making

## Usage

Use the SA-IQA inference script from the code repository:

```bash
python tools/infer.py --prompt_version 4 --mode all --dimension lighting
```

When running from the release repository root, the default model path is:

```text
SA-IQA-model/sa-iqa-prompt4
```

If this checkpoint is uploaded as a standalone Hugging Face model repository with the checkpoint files at the repository root, pass that local or Hub-downloaded checkpoint path through `--model_path`.

## Release Bundle Structure

```text
SA-IQA-model/
├── LICENSE
├── README.md
├── Ovis2.5-9B/
│   ├── LICENSE
│   ├── NOTICE
│   ├── config.json
│   ├── modeling_ovis2_5.py
│   ├── model-00001-of-00004.safetensors
│   ├── model-00002-of-00004.safetensors
│   ├── model-00003-of-00004.safetensors
│   ├── model-00004-of-00004.safetensors
│   └── ...
└── sa-iqa-prompt4/
    ├── config.json
    ├── modeling_ovis2_5.py
    ├── model-00001-of-00004.safetensors
    ├── model-00002-of-00004.safetensors
    ├── model-00003-of-00004.safetensors
    ├── model-00004-of-00004.safetensors
    └── ...
```

## Training Data

The model is fine-tuned and evaluated on SA-BENCH, an 18k-image benchmark for spatial aesthetics in interior scenes.

## Limitations

- The model is designed for interior images and may not generalize to other image domains.
- Predictions are based on the SA-BENCH annotation protocol and prompt design.
- The output should be treated as an assessment signal, not as a definitive human aesthetic judgment.

## License

The released SA-IQA model weights are governed by the custom non-commercial model license in `LICENSE`.

This model is fine-tuned from Ovis2.5-9B. Users must also comply with the base model license and notice files:

- `Ovis2.5-9B/LICENSE`
- `Ovis2.5-9B/NOTICE`

The Hugging Face metadata uses `license: other` because this model license is not one of the standard open-source license identifiers.

## Citation

If you use this model, please cite:

```bibtex
@inproceedings{gao2025beyond,
  title={Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics},
  author={Gao, Yuan and Song, Jin and Fei, Yiyun and Li, Gongzhe and Yang, Ruigao},
  booktitle={CVPR 2025 Workshop},
  year={2025}
}
```
