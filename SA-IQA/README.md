# SA-IQA

`SA-IQA` is the codebase released with the paper **“Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics.”**

It provides training, inference, and evaluation scripts for assessing the **spatial aesthetics** of interior images along four dimensions:

- **distortion**
- **harmony**
- **layout**
- **lighting**

The released final model in this project is **`sa-iqa-prompt4`**, corresponding to the recommended **prompt4** setting.

## Directory Structure

```text
SA-IQA/
├── LICENSE
├── README.md
├── requirements.txt
└── tools/
    ├── convert_csv_to_jsonl.py
    ├── evaluate_correlation_prompt1.py
    ├── evaluate_correlation_prompt2.py
    ├── evaluate_correlation_prompt3.py
    ├── evaluate_correlation_prompt4.py
    ├── infer_prompt1.py
    ├── infer_prompt2.py
    ├── infer_prompt3.py
    ├── infer_prompt4.py
    ├── infer_single_image_prompt4.py
    ├── train_sft_prompt1.sh
    ├── train_sft_prompt2.sh
    ├── train_sft_prompt3.sh
    └── train_sft_prompt4.sh
```

## Environment Setup

Install Python dependencies:

```bash
cd SA-IQA
pip install -r requirements.txt
```

> Note: packages such as PyTorch, DeepSpeed, and FlashAttention may require environment-specific installation depending on your CUDA version and hardware setup.

## Code Components

### Training Scripts

The following scripts are provided for supervised fine-tuning under different prompt settings:

- `tools/train_sft_prompt1.sh`
- `tools/train_sft_prompt2.sh`
- `tools/train_sft_prompt3.sh`
- `tools/train_sft_prompt4.sh`

Among them, **prompt4** is the recommended setting and corresponds to the released final model.

### Inference Scripts

The following scripts perform model inference and score generation:

- `tools/infer_prompt1.py`
- `tools/infer_prompt2.py`
- `tools/infer_prompt3.py`
- `tools/infer_prompt4.py`

For standard use in this release, we recommend using:

```bash
python tools/infer_prompt4.py --mode all --dimension lighting
```

### Single-Image Inference Script

- `tools/infer_single_image_prompt4.py`

This script supports direct inference on a single image using the released `sa-iqa-prompt4` model.

### Evaluation Scripts

The following scripts compute correlation metrics between predictions and ground-truth MOS:

- `tools/evaluate_correlation_prompt1.py`
- `tools/evaluate_correlation_prompt2.py`
- `tools/evaluate_correlation_prompt3.py`
- `tools/evaluate_correlation_prompt4.py`

### Conversion Tool

- `tools/convert_csv_to_jsonl.py`

This utility converts CSV annotations into prompt-based JSONL files for training or evaluation.

## Recommended Usage

The released final model is:

- `../SA-IQA-model/sa-iqa-prompt4`

The corresponding recommended inference script is:

- `tools/infer_prompt4.py`

The corresponding recommended single-image inference script is:

- `tools/infer_single_image_prompt4.py`

The corresponding recommended evaluation script is:

- `tools/evaluate_correlation_prompt4.py`

## Quick Start

### 1. Run Inference

From `SA-IQA/tools`:

```bash
cd SA-IQA/tools
python infer_prompt4.py --mode all --dimension lighting
```

Run the full pipeline for each dimension:

```bash
python infer_prompt4.py --mode all --dimension distortion
python infer_prompt4.py --mode all --dimension harmony
python infer_prompt4.py --mode all --dimension layout
python infer_prompt4.py --mode all --dimension lighting
```

### 2. Run Single-Image Inference

```bash
cd SA-IQA/tools
python infer_single_image_prompt4.py --image /path/to/image.jpg --dimension all
```

### 3. Run Overall Evaluation

Compute overall correlation across all four dimensions:

```bash
cd SA-IQA/tools
python evaluate_correlation_prompt4.py
```

### 4. Run Step-by-Step Modes

Inference only:

```bash
python infer_prompt4.py --mode infer --dimension lighting
```

Score conversion only:

```bash
python infer_prompt4.py --mode score --dimension lighting
```

Evaluation only:

```bash
python infer_prompt4.py --mode eval --dimension lighting
```

### 5. Explicitly Specify Paths

From `SA-IQA/tools`:

```bash
python infer_prompt4.py \
    --mode all \
    --dimension lighting \
    --model_path ../../SA-IQA-model/sa-iqa-prompt4 \
    --data_root ../../SA-BENCH \
    --results_dir ../results
```

From the project root:

```bash
python SA-IQA/tools/infer_prompt4.py \
    --mode all \
    --dimension lighting \
    --model_path ./SA-IQA-model/sa-iqa-prompt4 \
    --data_root ./SA-BENCH \
    --results_dir ./SA-IQA/results
```

### 6. Manually Specify Input and Output Files

```bash
python infer_prompt4.py \
    --mode all \
    --dimension lighting \
    --test_jsonl ../../SA-BENCH/annotations/lighting_3k_test_prompt4.jsonl \
    --input_csv ../../SA-BENCH/annotations/lighting_3k_test.csv \
    --output_jsonl ../results/lighting_prompt4_sa-iqa-prompt4.jsonl \
    --output_csv ../results/lighting_prompt4_sa-iqa-prompt4.csv
```

## Evaluation Metrics

The evaluation scripts report:

- **PLCC**: Pearson Linear Correlation Coefficient
- **SRCC**: Spearman Rank Correlation Coefficient

These metrics are used to measure the agreement between model predictions and human-annotated MOS scores.

## Results Directory

The `results/` directory stores:

- intermediate inference outputs in JSONL format
- scored CSV files for downstream evaluation

The output directory will be created automatically if it does not exist.

## Notes

- The released final model corresponds to **prompt4**.
- Prompt1, prompt2, and prompt3 scripts are mainly provided for comparison and ablation.
- Make sure `SA-BENCH` and `SA-IQA-model` are placed according to the release directory structure.
- Inference depends on the released model files and the base model files under `SA-IQA-model/`.

## License

Please refer to `LICENSE` for the code license.

## Citation

If you find this project useful, please cite:

```bibtex
@inproceedings{gao2025beyond,
  title={Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics},
  author={Gao, Yuan and Song, Jin and Fei, Yiyun and Li, Gongzhe and Yang, Ruigao},
  booktitle={CVPR 2025 Workshop},
  year={2025}
}
```

