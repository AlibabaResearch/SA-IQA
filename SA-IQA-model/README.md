---
license: apache-2.0
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

## Hugging Face Release Layout

This Hugging Face repository is released as a full model bundle. Download the whole repository to `./SA-IQA-model` when using it with the SA-IQA codebase.

The `sa-iqa-prompt4/` directory is the released final fine-tuned checkpoint for inference. The `Ovis2.5-9B/` directory is the bundled base model copy used by `tools/train_sft.sh` for training and reproducibility.

Because this repository contains two model directories, automatic loading from the repository root is not expected to work. Load the fine-tuned checkpoint from `SA-IQA-model/sa-iqa-prompt4`, or pass that path through the SA-IQA inference script with `--model_path`.

## Model Details

### Model Description

- **Model type:** multimodal vision-language model for image quality assessment
- **Base model:** Ovis2.5-9B
- **Fine-tuned checkpoint:** sa-iqa-prompt4
- **Input:** image plus a dimension-specific text prompt
- **Output:** textual quality label and token log-probabilities used to compute a continuous score
- **Dimensions:** distortion, harmony, layout, lighting

### Intended Use

SA-IQA is intended for research, evaluation, and application use, including:

- spatial aesthetic assessment of interior images
- image quality benchmarking on SA-BENCH
- reward-model research for image generation and best-of-N selection
- comparison of prompt variants for spatial aesthetic assessment

### Out-of-Scope Use

The model is not intended for:

- universal aesthetic judgment outside the interior-scene domain
- safety-critical or legally binding decision making

## Usage

Use the SA-IQA inference script from the code repository:

```bash
python tools/infer.py --prompt_version 4 --mode all --dimension lighting
```

When running from the release bundle root, the default model path is:

```text
SA-IQA-model/sa-iqa-prompt4
```

If you downloaded this Hugging Face repository to another local path, pass the nested `sa-iqa-prompt4` checkpoint path through `--model_path`.

## Release Bundle Structure

```text
SA-IQA-model/
├── LICENSE
├── README.md
├── Ovis2.5-9B/                  # Base model used by training scripts
│   ├── LICENSE
│   ├── NOTICE
│   ├── config.json
│   ├── modeling_ovis2_5.py
│   ├── model-00001-of-00004.safetensors
│   ├── model-00002-of-00004.safetensors
│   ├── model-00003-of-00004.safetensors
│   ├── model-00004-of-00004.safetensors
│   └── ...
└── sa-iqa-prompt4/              # Fine-tuned checkpoint used for inference
    ├── config.json
    ├── modeling_ovis2_5.py
    ├── model-00001-of-00004.safetensors
    ├── model-00002-of-00004.safetensors
    ├── model-00003-of-00004.safetensors
    ├── model-00004-of-00004.safetensors
    └── ...
```

## Training Data

The model is fine-tuned and evaluated on SA-BENCH, a 17,768-example benchmark for spatial aesthetics in interior scenes.

## Limitations

- The model is designed for interior images and may not generalize to other image domains.
- Predictions are based on the SA-BENCH annotation protocol and prompt design.
- The output should be treated as an assessment signal, not as a definitive human aesthetic judgment.

## License

The released SA-IQA model weights are licensed under the Apache License 2.0. See `LICENSE` for the full license text.

This model is fine-tuned from Ovis2.5-9B, which is also released under the Apache License 2.0. When redistributing or modifying this model, retain attribution and relevant notices from the base model:

- `Ovis2.5-9B/LICENSE`
- `Ovis2.5-9B/NOTICE`

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
