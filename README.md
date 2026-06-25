# SA-IQA

Official release for **“Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics.”**

Project documentation is being updated.

SA-IQA evaluates the spatial aesthetics of interior images along four dimensions:

- **distortion**
- **harmony**
- **layout**
- **lighting**

This repository contains the SA-IQA code. The released model bundle and SA-BENCH dataset are hosted on Hugging Face:

- Model bundle: `AliHome3D/SA-IQA-model`
- Dataset: `AliHome3D/SA-BENCH`

## Repository Structure

```text
SA-IQA/
├── LICENSE
├── README.md
├── requirements.txt
├── tools/
│   ├── convert_csv_to_jsonl.py
│   ├── evaluate_correlation.py
│   ├── infer.py
│   ├── local_progress.py
│   ├── prompt_configs.py
│   └── train_sft.sh
├── SA-BENCH/                 # Downloaded from AliHome3D/SA-BENCH
│   ├── LICENSE
│   ├── README.md
│   ├── annotations/
│   └── images/
└── SA-IQA-model/             # Downloaded from AliHome3D/SA-IQA-model
    ├── LICENSE
    ├── README.md
    ├── Ovis2.5-9B/
    └── sa-iqa-prompt4/
```

## Installation

```bash
conda create -n sa-iqa python=3.10 -y
conda activate sa-iqa
pip install -r requirements.txt
```

`requirements.txt` contains inference, scoring, evaluation, and data-conversion dependencies. It installs `torch==2.5.1+cu124`, the matching `torchvision`/`torchaudio` wheels, `flash-attn==2.7.4.post1`, and pins `ms-swift` to the 3.x API because the current inference code uses `swift.llm`.

Training with `tools/train_sft.sh` additionally requires a CUDA-compatible training stack such as DeepSpeed.

## Download Model and Dataset

Install the Hugging Face Hub CLI if it is not already available:

```bash
pip install -U huggingface_hub
```

From the repository root, download the model bundle and dataset into the expected local directory names:

```bash
hf download AliHome3D/SA-IQA-model \
  --repo-type model \
  --local-dir SA-IQA-model

hf download AliHome3D/SA-BENCH \
  --repo-type dataset \
  --local-dir SA-BENCH
```

The local layout should be:

```text
SA-IQA/
├── SA-IQA-model/
│   ├── Ovis2.5-9B/
│   └── sa-iqa-prompt4/
└── SA-BENCH/
    ├── annotations/
    └── images/
```

Keep these directory names if you want to use the default script arguments. `tools/infer.py` loads `./SA-IQA-model/sa-iqa-prompt4` by default for prompt 4, and `tools/train_sft.sh` uses `./SA-IQA-model/Ovis2.5-9B` as the default base model.

If you download the files to another location, pass explicit paths through `--model_path`, `--data_root`, or `--model`.

## Inference

Run inference with the released `sa-iqa-prompt4` model:

```bash
python tools/infer.py --prompt_version 4 --mode all --dimension lighting
```

This command uses:

- model: `./SA-IQA-model/sa-iqa-prompt4`
- data: `./SA-BENCH`
- test split: `./SA-BENCH/annotations/lighting_3k_test_prompt4.jsonl`
- output: `./results/lighting_prompt4_sa-iqa-prompt4.jsonl` and `./results/lighting_prompt4_sa-iqa-prompt4.csv`

Run all four dimensions:

```bash
python tools/infer.py --prompt_version 4 --mode all --dimension distortion
python tools/infer.py --prompt_version 4 --mode all --dimension harmony
python tools/infer.py --prompt_version 4 --mode all --dimension layout
python tools/infer.py --prompt_version 4 --mode all --dimension lighting
```

By default, outputs are written under `results/`.

For a quick smoke test, reduce the inference batch size if GPU memory is limited:

```bash
python tools/infer.py --prompt_version 4 --mode all --dimension lighting --batch_size 1 --max_batch_size 1
```

## Step-By-Step Modes

Inference only:

```bash
python tools/infer.py --prompt_version 4 --mode infer --dimension lighting
```

Score conversion only:

```bash
python tools/infer.py --prompt_version 4 --mode score --dimension lighting
```

Per-dimension evaluation only:

```bash
python tools/infer.py --prompt_version 4 --mode eval --dimension lighting
```

Overall evaluation across all four dimensions:

```bash
python tools/evaluate_correlation.py --prompt_version 4
```

## Training

Use the unified training entrypoint:

```bash
bash tools/train_sft.sh --prompt_version 4
```

The default training base model path is `./SA-IQA-model/Ovis2.5-9B`, so download `AliHome3D/SA-IQA-model` as the full bundle before training. The default output path for prompt 4 is `./SA-IQA-model/sa-iqa-prompt4`.

Prompt1, prompt2, and prompt3 are available through `--prompt_version` for comparison and ablation. Prompt4 is the recommended setting and corresponds to the released final model.

## Data Conversion

`tools/convert_csv_to_jsonl.py` converts annotation CSV files into prompt-based JSONL files for training or evaluation.

## Licenses

- Code in this repository root and `tools/` is licensed under the Apache License 2.0. See `LICENSE`.
- `SA-BENCH/` is licensed under the Apache License 2.0. See `SA-BENCH/LICENSE`.
- `SA-IQA-model/` is licensed under the Apache License 2.0. See `SA-IQA-model/LICENSE`.
- `SA-IQA-model/Ovis2.5-9B/` is the bundled base model copy and retains its original Apache License 2.0 license and notice files.

The repository-level `CITATION.cff` license field applies to the code release. Dataset and model usage are governed by their own license files.

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
