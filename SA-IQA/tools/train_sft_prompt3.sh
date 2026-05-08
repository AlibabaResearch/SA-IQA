#!/usr/bin/env bash

CUDA_VISIBLE_DEVICES=0,1,2,3 MASTER_PORT=29503 NPROC_PER_NODE=4 swift sft \
    --model_type ovis2_5 \
    --model ../SA-IQA-model/Ovis2.5-9B \
    --train_type full \
    --freeze_llm false \
    --freeze_vit true \
    --freeze_aligner true \
    --dataset \
        ../SA-BENCH/annotations/distortion_2k_train_prompt3.jsonl \
        ../SA-BENCH/annotations/harmony_7k_train_prompt3.jsonl \
        ../SA-BENCH/annotations/layout_6k_train_prompt3.jsonl \
        ../SA-BENCH/annotations/lighting_3k_train_prompt3.jsonl \
    --val_dataset \
        ../SA-BENCH/annotations/distortion_2k_test_prompt3.jsonl \
        ../SA-BENCH/annotations/harmony_7k_test_prompt3.jsonl \
        ../SA-BENCH/annotations/layout_6k_test_prompt3.jsonl \
        ../SA-BENCH/annotations/lighting_3k_test_prompt3.jsonl \
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
    --output_dir ../SA-IQA-model/sa-iqa-prompt3 \
    --system 'You are a helpful assistant.' \
    --warmup_ratio 0.03 \
    --dataloader_num_workers 4
