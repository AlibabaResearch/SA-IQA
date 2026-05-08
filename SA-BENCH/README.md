# SA-BENCH

`SA-BENCH` is the benchmark dataset released with the paper **“Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics.”**

It is designed for evaluating the **spatial aesthetics** of interior images along four dimensions:

- **distortion**
- **harmony**
- **layout**
- **lighting**

The dataset contains **18,000 images** and corresponding annotations for training and evaluation.

## Directory Structure

```text
SA-BENCH/
├── LICENSE
├── README.md
├── annotations/
│   ├── distortion_2k_full.csv
│   ├── distortion_2k_test.csv
│   ├── distortion_2k_test_prompt1.jsonl
│   ├── distortion_2k_test_prompt2.jsonl
│   ├── distortion_2k_test_prompt3.jsonl
│   ├── distortion_2k_test_prompt4.jsonl
│   ├── distortion_2k_train.csv
│   ├── distortion_2k_train_prompt1.jsonl
│   ├── distortion_2k_train_prompt2.jsonl
│   ├── distortion_2k_train_prompt3.jsonl
│   ├── distortion_2k_train_prompt4.jsonl
│   ├── harmony_7k_full.csv
│   ├── harmony_7k_test.csv
│   ├── harmony_7k_test_prompt1.jsonl
│   ├── harmony_7k_test_prompt2.jsonl
│   ├── harmony_7k_test_prompt3.jsonl
│   ├── harmony_7k_test_prompt4.jsonl
│   ├── harmony_7k_train.csv
│   ├── harmony_7k_train_prompt1.jsonl
│   ├── harmony_7k_train_prompt2.jsonl
│   ├── harmony_7k_train_prompt3.jsonl
│   ├── harmony_7k_train_prompt4.jsonl
│   ├── layout_6k_full.csv
│   ├── layout_6k_test.csv
│   ├── layout_6k_test_prompt1.jsonl
│   ├── layout_6k_test_prompt2.jsonl
│   ├── layout_6k_test_prompt3.jsonl
│   ├── layout_6k_test_prompt4.jsonl
│   ├── layout_6k_train.csv
│   ├── layout_6k_train_prompt1.jsonl
│   ├── layout_6k_train_prompt2.jsonl
│   ├── layout_6k_train_prompt3.jsonl
│   ├── layout_6k_train_prompt4.jsonl
│   ├── lighting_3k_full.csv
│   ├── lighting_3k_test.csv
│   ├── lighting_3k_test_prompt1.jsonl
│   ├── lighting_3k_test_prompt2.jsonl
│   ├── lighting_3k_test_prompt3.jsonl
│   ├── lighting_3k_test_prompt4.jsonl
│   ├── lighting_3k_train.csv
│   ├── lighting_3k_train_prompt1.jsonl
│   ├── lighting_3k_train_prompt2.jsonl
│   ├── lighting_3k_train_prompt3.jsonl
│   └── lighting_3k_train_prompt4.jsonl
└── images/
    ├── distortion/
    ├── harmony/
    ├── layout/
    └── lighting/
```

## Dataset Overview

SA-BENCH organizes interior images into four spatial aesthetic dimensions:

- **distortion**: evaluates geometric distortion, deformation, alignment errors, and material realism
- **harmony**: evaluates style consistency, color coordination, and overall visual coherence
- **layout**: evaluates spatial arrangement, balance, and positional relationships of key elements
- **lighting**: evaluates illumination quality, shadow realism, light-source consistency, and atmosphere

Each dimension includes:

- image files
- CSV annotations
- prompt-based JSONL files for model training and evaluation

## Annotation Files

The `annotations/` directory provides CSV files for each dimension.

### CSV Files

For each dimension, three CSV files are provided:

- `*_train.csv`: training split
- `*_test.csv`: test split
- `*_full.csv`: full set

These CSV files contain image identifiers and corresponding annotation fields used for training and evaluation.

## Prompt-based JSONL Files

For each dimension and split, we provide JSONL files corresponding to four prompt variants:

- `prompt1`
- `prompt2`
- `prompt3`
- `prompt4`

These files are used by the SA-IQA training and inference scripts.

Examples:

- `lighting_3k_train_prompt4.jsonl`
- `layout_6k_test_prompt4.jsonl`

Among the four prompt variants, **prompt4** is the recommended setting and corresponds to the released final model `sa-iqa-prompt4`.

## Data Splits

The dataset includes the following subsets:

- **distortion**: 2k
- **harmony**: 7k
- **layout**: 6k
- **lighting**: 3k

Together they form an 18k-image benchmark for spatial aesthetics evaluation.

## Usage

This dataset is intended for:

- benchmarking image quality and aesthetic assessment methods on interior scenes
- training multimodal models for spatial aesthetics evaluation
- evaluating dimension-specific quality prediction
- reward modeling for image generation and selection tasks

## Used in This Release

In this release:

- `SA-BENCH` provides the data source
- `SA-IQA/tools/` provides scripts for training, inference, and evaluation
- `SA-IQA-model/sa-iqa-prompt4` is the released final model corresponding to the recommended **prompt4** setting

## Notes

- Image paths referenced in the JSONL files are organized to work with the provided inference scripts in `SA-IQA/tools/`.
- Prompt-based JSONL files are provided for reproducibility and direct use in training and evaluation.
- For standard evaluation in this release, we recommend using the `prompt4` files.

## License

Please refer to `LICENSE` for the dataset license and usage terms.

## Citation

If you find SA-BENCH useful, please cite:

```bibtex
@inproceedings{gao2025beyond,
  title={Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics},
  author={Gao, Yuan and Song, Jin and Fei, Yiyun and Li, Gongzhe and Yang, Ruigao},
  booktitle={CVPR 2025 Workshop},
  year={2025}
}
```

