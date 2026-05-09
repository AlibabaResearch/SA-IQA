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
    ├── evaluate_correlation.py
    ├── infer.py
    ├── local_progress.py
    ├── prompt_configs.py
    └── train_sft.sh
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

Use the unified training script for supervised fine-tuning under different prompt settings:

```bash
bash tools/train_sft.sh --prompt_version 4
```

Among the prompt variants, **prompt4** is the recommended setting and corresponds to the released final model.

### Inference Scripts

Use the unified inference script for model inference and score generation:

```bash
python tools/infer.py --prompt_version 4 --mode all --dimension lighting
```

### Evaluation Scripts

Use the unified evaluation script to compute correlation metrics between predictions and ground-truth MOS:

```bash
python tools/evaluate_correlation.py --prompt_version 4
```

### Conversion Tool

- `tools/convert_csv_to_jsonl.py`

This utility converts CSV annotations into prompt-based JSONL files for training or evaluation.

## Recommended Usage

The released final model is:

- `../SA-IQA-model/sa-iqa-prompt4`

The corresponding recommended inference script is:

- `tools/infer.py --prompt_version 4`

The corresponding recommended evaluation script is:

- `tools/evaluate_correlation.py --prompt_version 4`

## Quick Start

### 1. Run Inference

From `SA-IQA/tools`:

```bash
cd SA-IQA/tools
python infer.py --prompt_version 4 --mode all --dimension lighting
```

Run the full pipeline for each dimension:

```bash
python infer.py --prompt_version 4 --mode all --dimension distortion
python infer.py --prompt_version 4 --mode all --dimension harmony
python infer.py --prompt_version 4 --mode all --dimension layout
python infer.py --prompt_version 4 --mode all --dimension lighting
```

### 2. Run Overall Evaluation

Compute overall correlation across all four dimensions:

```bash
cd SA-IQA/tools
python evaluate_correlation.py --prompt_version 4
```

### 3. Run Step-by-Step Modes

Inference only:

```bash
python infer.py --prompt_version 4 --mode infer --dimension lighting
```

Score conversion only:

```bash
python infer.py --prompt_version 4 --mode score --dimension lighting
```

Evaluation only:

```bash
python infer.py --prompt_version 4 --mode eval --dimension lighting
```

### 4. Explicitly Specify Paths

From `SA-IQA/tools`:

```bash
python infer.py \
    --prompt_version 4 \
    --mode all \
    --dimension lighting \
    --model_path ../../SA-IQA-model/sa-iqa-prompt4 \
    --data_root ../../SA-BENCH \
    --results_dir ../results
```

From the project root:

```bash
python SA-IQA/tools/infer.py \
    --prompt_version 4 \
    --mode all \
    --dimension lighting \
    --model_path ./SA-IQA-model/sa-iqa-prompt4 \
    --data_root ./SA-BENCH \
    --results_dir ./SA-IQA/results
```

### 5. Manually Specify Input and Output Files

```bash
python infer.py \
    --prompt_version 4 \
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
- Prompt1, prompt2, and prompt3 are available through `--prompt_version` for comparison and ablation.
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
