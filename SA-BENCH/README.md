---
license: apache-2.0
pretty_name: SA-BENCH
language:
  - en
task_categories:
  - image-classification
size_categories:
  - 10K<n<100K
tags:
  - image
  - image-quality-assessment
  - aesthetics
  - spatial-aesthetics
  - interior-design
  - benchmark
configs:
  - config_name: distortion
    data_files:
      - split: train
        path: annotations/distortion_2k_train.csv
      - split: test
        path: annotations/distortion_2k_test.csv
      - split: full
        path: annotations/distortion_2k_full.csv
  - config_name: harmony
    data_files:
      - split: train
        path: annotations/harmony_7k_train.csv
      - split: test
        path: annotations/harmony_7k_test.csv
      - split: full
        path: annotations/harmony_7k_full.csv
  - config_name: layout
    data_files:
      - split: train
        path: annotations/layout_6k_train.csv
      - split: test
        path: annotations/layout_6k_test.csv
      - split: full
        path: annotations/layout_6k_full.csv
  - config_name: lighting
    data_files:
      - split: train
        path: annotations/lighting_3k_train.csv
      - split: test
        path: annotations/lighting_3k_test.csv
      - split: full
        path: annotations/lighting_3k_full.csv
---

# SA-BENCH

SA-BENCH is the benchmark dataset released with **“Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics.”**

It evaluates the spatial aesthetics of interior images along four dimensions:

- **distortion**
- **harmony**
- **layout**
- **lighting**

The dataset contains **17,768 annotated examples** across four spatial-aesthetic dimensions, with image assets and human annotations for training and evaluation.

## Dataset Details

### Dataset Description

SA-BENCH is designed for image quality and aesthetic assessment of interior scenes. It focuses on spatial aesthetics rather than generic image appeal, and provides dimension-specific annotations for:

- **distortion**: geometric distortion, deformation, alignment errors, and material realism
- **harmony**: style consistency, color coordination, and overall visual coherence
- **layout**: spatial arrangement, balance, and positional relationships of key elements
- **lighting**: illumination quality, shadow realism, light-source consistency, and atmosphere

### Dataset Sources

- Repository: this Hugging Face dataset repository
- Associated paper: **Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics**
- Code and model release: SA-IQA

## Dataset Structure

```text
SA-BENCH/
├── LICENSE
├── README.md
├── annotations/
│   ├── distortion_2k_train.csv
│   ├── distortion_2k_test.csv
│   ├── distortion_2k_full.csv
│   ├── harmony_7k_train.csv
│   ├── harmony_7k_test.csv
│   ├── harmony_7k_full.csv
│   ├── layout_6k_train.csv
│   ├── layout_6k_test.csv
│   ├── layout_6k_full.csv
│   ├── lighting_3k_train.csv
│   ├── lighting_3k_test.csv
│   ├── lighting_3k_full.csv
│   └── *_prompt{1,2,3,4}.jsonl
└── images/
    ├── distortion/images/
    ├── harmony/images/
    ├── layout/images/
    └── lighting/images/
```

### Data Fields

The CSV annotation files contain:

- `id`: image identifier
- `{dimension}_score_*`: individual human annotation scores
- `{dimension}_score_mos`: mean opinion score
- `{dimension}_score_mos_int`: integer-rounded MOS label used for prompt-response generation
- `model`: source generation model, when available for that dimension

The JSONL prompt files contain:

- `query`: prompt text
- `response`: target textual quality label
- `images`: image path list used by the accompanying SA-IQA codebase

The JSONL `images` values intentionally keep the `SA-BENCH/` prefix, for example `SA-BENCH/images/distortion/images/distortion_1025.jpg`. This matches the expected layout when the dataset directory is used together with the SA-IQA code from the parent project directory. When loading files from inside the Hugging Face dataset repository root directly, strip the leading `SA-BENCH/` prefix or prepend the parent directory accordingly.

### Data Splits

Each dimension provides `train`, `test`, and `full` CSV splits:

| Dimension | Subset | Description |
| --- | --- | --- |
| distortion | 2,226 | Spatial distortion quality |
| harmony | 6,741 | Style and color harmony quality |
| layout | 5,556 | Spatial layout quality |
| lighting | 3,245 | Lighting quality |

Together they form a 17,768-example benchmark.

## Usage

The CSV files can be loaded directly through the Hugging Face Dataset Viewer using the metadata configurations above. Prompt-based JSONL files are also included for reproducibility and direct use with SA-IQA training/evaluation scripts.

For standard evaluation in this release, use the `prompt4` files with the released `sa-iqa-prompt4` model.

## Intended Use

SA-BENCH is intended for:

- non-commercial research on image quality assessment
- benchmarking spatial aesthetic assessment methods
- training and evaluating multimodal models for interior-image quality prediction
- reward-model research for image generation and selection

## Limitations

- The dataset focuses on interior-scene imagery and may not generalize to portraits, landscapes, or general artistic images.
- Scores reflect the annotation protocol used for this benchmark and should not be treated as universal aesthetic judgments.
- Users should evaluate fairness, safety, and domain suitability before applying models trained on this dataset to new data.

## License

SA-BENCH is released under the Apache License 2.0. See `LICENSE` for the full license text.

## Citation

If you use SA-BENCH, please cite:

```bibtex
@inproceedings{gao2025beyond,
  title={Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics},
  author={Gao, Yuan and Song, Jin and Fei, Yiyun and Li, Gongzhe and Yang, Ruigao},
  booktitle={CVPR 2025 Workshop},
  year={2025}
}
```
