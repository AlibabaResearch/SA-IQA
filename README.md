# SA-IQA Release

This repository accompanies the paper **“Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics.”**

We introduce **Spatial Aesthetics**, a new paradigm for evaluating the aesthetic quality of interior images along four dimensions:

- **distortion**
- **harmony**
- **layout**
- **lighting**

This release package contains the **SA-BENCH dataset**, the **SA-IQA codebase**, and the **trained SA-IQA model**.

## Paper

**Title:** Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics

**Authors:** Yuan Gao, Jin Song, Yiyun Fei, Gongzhe Li, Ruigao Yang

**Affiliations:**  
1 Alibaba Group  
2 The Chinese University of Hong Kong, Shenzhen

**Contact:**  
gaoyuan20@mails.ucas.ac.cn  
songjin.song@alibaba-inc.com  
yunhun.fyy@alibaba-inc.com  
gongzheli1@link.cuhk.edu.cn  
ruigao.yrg@alibaba-inc.com

**Status:** Accepted at a CVPR 2025 workshop.

**Abstract:**  
In recent years, Image Quality Assessment (IQA) for AI-generated images (AIGI) has advanced rapidly; however, existing methods primarily target portraits and artistic images, lacking a systematic evaluation of interior scenes. We introduce Spatial Aesthetics, a paradigm that assesses the aesthetic quality of interior images along four dimensions: layout, harmony, lighting, and distortion. We construct SA-BENCH, the first benchmark for spatial aesthetics, comprising 18,000 images and 50,000 precise annotations. Employing SA-BENCH, we systematically evaluate current IQA methodologies and develop SA-IQA, through MLLM fine-tuning and a multidimensional fusion approach, as a comprehensive reward framework for assessing spatial aesthetics. We apply SA-IQA to two downstream tasks: (1) serving as a reward signal integrated with GRPO reinforcement learning to optimize the AIGC generation pipeline, and (2) Best-of-N selection to filter high-quality images and improve generation quality. Experiments indicate that SA-IQA significantly outperforms existing methods on SA-BENCH, setting a new standard for spatial aesthetics evaluation. Code and dataset are released to advance research and applications in this domain.

## Repository Structure

```text
SA-IQA-Release/
├── README.md
├── SA-BENCH/       # Dataset
├── SA-IQA/         # Codebase
└── SA-IQA-model/   # Base model and trained SA-IQA model
```

## Components

### SA-BENCH

`SA-BENCH` contains:

- annotation CSV files
- prompt-based JSONL files for training and evaluation
- image folders for four spatial aesthetic dimensions:
  - distortion
  - harmony
  - layout
  - lighting

See [SA-BENCH/README.md](./SA-BENCH/README.md) for details.

### SA-IQA

`SA-IQA` contains:

- training scripts
- inference scripts
- evaluation scripts
- single-image inference script
- CSV-to-JSONL conversion tool
- Python requirements

See [SA-IQA/README.md](./SA-IQA/README.md) for details.

### SA-IQA-model

`SA-IQA-model` contains:

- the base model `Ovis2.5-9B`
- the released trained model `sa-iqa-prompt4`

Among the four prompt variants, **prompt4** is the recommended setting and `sa-iqa-prompt4` is the final model used for inference. The other prompt versions are mainly provided for ablation and comparison purposes.

See [SA-IQA-model/README.md](./SA-IQA-model/README.md) for details.

## Download and Placement

Please organize the files under the following directory structure:

```text
SA-IQA-Release/
├── SA-BENCH/
├── SA-IQA/
└── SA-IQA-model/
```

The default paths used by the provided scripts assume this structure.

If `SA-BENCH` and `SA-IQA-model` are hosted separately, please download them and place them under the same root directory as `SA-IQA`.

## Quick Start

### 1. Install Dependencies

```bash
cd SA-IQA
pip install -r requirements.txt
```

> Note: packages such as PyTorch, DeepSpeed, and FlashAttention may require environment-specific installation depending on your CUDA version and hardware setup.

### 2. Run Inference

Run inference with the released `sa-iqa-prompt4` model:

```bash
cd SA-IQA/tools
python infer_prompt4.py --mode all --dimension lighting
```

Run all four dimensions:

```bash
python infer_prompt4.py --mode all --dimension distortion
python infer_prompt4.py --mode all --dimension harmony
python infer_prompt4.py --mode all --dimension layout
python infer_prompt4.py --mode all --dimension lighting
```

### 3. Run Single-Image Inference

```bash
cd SA-IQA/tools
python infer_single_image_prompt4.py --image /path/to/image.jpg --dimension all
```

### 4. Run Overall Evaluation

Compute overall correlation across all four dimensions:

```bash
cd SA-IQA/tools
python evaluate_correlation_prompt4.py
```

## Release Contents

This release includes:

- **SA-BENCH**, a benchmark for spatial aesthetics in interior images
- **SA-IQA**, a codebase for training, inference, and evaluation
- **sa-iqa-prompt4**, the released trained model for practical use

## Notes

- `SA-IQA-model/sa-iqa-prompt4` is the released trained model used for inference.
- Prompt-specific training and inference scripts are provided in `SA-IQA/tools/`.
- `infer_single_image_prompt4.py` supports direct inference on a single image.
- The `results/` folder in `SA-IQA/` stores intermediate inference outputs and scored CSV files.
- For standard usage, we recommend directly using **prompt4**.
- This project uses `Ovis2.5-9B` as the base model. Please comply with its original license and notice files when using the released model.

## License

- `SA-IQA/` is released under its own code license.
- `SA-BENCH/` is released under its own dataset license.
- `SA-IQA-model/` is released under its own model license.
- The base model `Ovis2.5-9B` remains subject to its original license and notice files.

Please refer to the corresponding `LICENSE` files in each subdirectory for details.

## Citation

If you find this project useful, please cite our work.

```bibtex
@inproceedings{gao2025beyond,
  title={Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics},
  author={Gao, Yuan and Song, Jin and Fei, Yiyun and Li, Gongzhe and Yang, Ruigao},
  booktitle={CVPR 2025 Workshop},
  year={2025}
}
```
