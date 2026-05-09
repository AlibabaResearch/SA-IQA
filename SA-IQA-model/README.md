# SA-IQA-model

`SA-IQA-model` contains the base model and the released trained model for the paper **“Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics.”**

## Contents

This directory includes:

- **`Ovis2.5-9B/`**: the base multimodal model used in this project
- **`sa-iqa-prompt4/`**: the released trained SA-IQA model checkpoint

## Model Description

### `Ovis2.5-9B`

`Ovis2.5-9B` is the base model used for SA-IQA training and inference.

This directory contains the original files required to load the base architecture, tokenizer, processor, and model weights.

### `sa-iqa-prompt4`

`sa-iqa-prompt4` is the released final SA-IQA model used for inference in this release.

Among the four prompt variants studied in the paper, **prompt4** is the recommended setting and `sa-iqa-prompt4` is the final model for standard usage.

## Recommended Usage

For standard use, please run inference with:

- model: `sa-iqa-prompt4`
- inference script: `../SA-IQA/tools/infer.py --prompt_version 4`

## Example Usage

Run dimension-wise inference:

```bash
cd ../SA-IQA/tools
python infer.py --prompt_version 4 --mode all --dimension lighting
```

Specify the model path explicitly:

```bash
cd ../SA-IQA/tools
python infer.py \
    --prompt_version 4 \
    --mode all \
    --dimension lighting \
    --model_path ../../SA-IQA-model/sa-iqa-prompt4
```

## Directory Structure

```text
SA-IQA-model/
├── LICENSE
├── Ovis2.5-9B/
│   ├── LICENSE
│   ├── NOTICE
│   ├── README.md
│   ├── added_tokens.json
│   ├── chat_template.json
│   ├── config.json
│   ├── configuration_ovis2_5.py
│   ├── generation_config.json
│   ├── merges.txt
│   ├── model-00001-of-00004.safetensors
│   ├── model-00002-of-00004.safetensors
│   ├── model-00003-of-00004.safetensors
│   ├── model-00004-of-00004.safetensors
│   ├── model.safetensors.index.json
│   ├── modeling_ovis2_5.py
│   ├── preprocessor_config.json
│   ├── special_tokens_map.json
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   └── vocab.json
└── sa-iqa-prompt4/
    ├── added_tokens.json
    ├── args.json
    ├── chat_template.jinja
    ├── config.json
    ├── configuration_ovis2_5.py
    ├── generation_config.json
    ├── merges.txt
    ├── model-00001-of-00004.safetensors
    ├── model-00002-of-00004.safetensors
    ├── model-00003-of-00004.safetensors
    ├── model-00004-of-00004.safetensors
    ├── model.safetensors.index.json
    ├── modeling_ovis2_5.py
    ├── preprocessor_config.json
    ├── special_tokens_map.json
    ├── tokenizer.json
    ├── tokenizer_config.json
    └── vocab.json
```

## Notes

- `sa-iqa-prompt4` is the released final model checkpoint for practical inference.
- `Ovis2.5-9B` is the base model dependency used by this project.
- Please make sure both the base model files and the trained model files are correctly placed under `SA-IQA-model/`.
- The SA-IQA codebase uses this directory structure as the default model path setting.

## License

The released SA-IQA model is provided under the license in `SA-IQA-model/LICENSE`.

The base model `Ovis2.5-9B` is subject to its original license and notice files:

- `Ovis2.5-9B/LICENSE`
- `Ovis2.5-9B/NOTICE`

Please ensure compliance with both the released model license and the base model license when using this model.

## Citation

If you find this model useful, please cite:

```bibtex
@inproceedings{gao2025beyond,
  title={Beyond Pixels: Benchmarking and Reward-Based Assessing Framework for Visual Spatial Aesthetics},
  author={Gao, Yuan and Song, Jin and Fei, Yiyun and Li, Gongzhe and Yang, Ruigao},
  booktitle={CVPR 2025 Workshop},
  year={2025}
}
```
