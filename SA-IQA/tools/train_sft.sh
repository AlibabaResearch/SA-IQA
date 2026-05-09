#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: bash train_sft.sh --prompt_version {1|2|3|4} [options]

Options:
  --prompt_version N          Prompt version to train. Required.
  --cuda_visible_devices IDS  GPU ids. Defaults match the original prompt scripts.
  --master_port PORT          Distributed master port. Defaults to 29500 + prompt version.
  --nproc_per_node N          Number of processes per node. Default: 4.
  --model PATH                Base model path. Default: ../SA-IQA-model/Ovis2.5-9B.
  --output_dir PATH           Output path. Default: ../SA-IQA-model/sa-iqa-promptN.
  -h, --help                  Show this help.

Unknown options are forwarded to swift sft.
EOF
}

prompt_version=""
cuda_visible_devices=""
master_port=""
nproc_per_node=4
model="../SA-IQA-model/Ovis2.5-9B"
output_dir=""
extra_args=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --prompt_version)
            prompt_version="$2"
            shift 2
            ;;
        --cuda_visible_devices)
            cuda_visible_devices="$2"
            shift 2
            ;;
        --master_port)
            master_port="$2"
            shift 2
            ;;
        --nproc_per_node)
            nproc_per_node="$2"
            shift 2
            ;;
        --model)
            model="$2"
            shift 2
            ;;
        --output_dir)
            output_dir="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            extra_args+=("$1")
            shift
            ;;
    esac
done

case "$prompt_version" in
    1|2|3|4)
        ;;
    "")
        echo "Error: --prompt_version is required." >&2
        usage >&2
        exit 2
        ;;
    *)
        echo "Error: --prompt_version must be one of 1, 2, 3, 4." >&2
        exit 2
        ;;
esac

if [[ -z "$cuda_visible_devices" ]]; then
    case "$prompt_version" in
        1|3) cuda_visible_devices="0,1,2,3" ;;
        2|4) cuda_visible_devices="4,5,6,7" ;;
    esac
fi

if [[ -z "$master_port" ]]; then
    master_port=$((29500 + prompt_version))
fi

if [[ -z "$output_dir" ]]; then
    output_dir="../SA-IQA-model/sa-iqa-prompt${prompt_version}"
fi

CUDA_VISIBLE_DEVICES="$cuda_visible_devices" MASTER_PORT="$master_port" NPROC_PER_NODE="$nproc_per_node" swift sft \
    --model_type ovis2_5 \
    --model "$model" \
    --train_type full \
    --freeze_llm false \
    --freeze_vit true \
    --freeze_aligner true \
    --dataset \
        "../SA-BENCH/annotations/distortion_2k_train_prompt${prompt_version}.jsonl" \
        "../SA-BENCH/annotations/harmony_7k_train_prompt${prompt_version}.jsonl" \
        "../SA-BENCH/annotations/layout_6k_train_prompt${prompt_version}.jsonl" \
        "../SA-BENCH/annotations/lighting_3k_train_prompt${prompt_version}.jsonl" \
    --val_dataset \
        "../SA-BENCH/annotations/distortion_2k_test_prompt${prompt_version}.jsonl" \
        "../SA-BENCH/annotations/harmony_7k_test_prompt${prompt_version}.jsonl" \
        "../SA-BENCH/annotations/layout_6k_test_prompt${prompt_version}.jsonl" \
        "../SA-BENCH/annotations/lighting_3k_test_prompt${prompt_version}.jsonl" \
    --torch_dtype bfloat16 \
    --deepspeed zero2 \
    --attn_impl flash_attn \
    --padding_free true \
    --num_train_epochs 3 \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 32 \
    --eval_steps 10 \
    --save_steps 1000 \
    --save_total_limit 1 \
    --learning_rate 2e-5 \
    --logging_steps 1 \
    --max_length 2048 \
    --output_dir "$output_dir" \
    --system 'You are a helpful assistant.' \
    --warmup_ratio 0.03 \
    --dataloader_num_workers 4 \
    "${extra_args[@]}"
