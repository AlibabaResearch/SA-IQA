import argparse
import json
import math
import os

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

from local_progress import progress_iter
from swift.llm import PtEngine, RequestConfig, InferRequest


LABELS = ["excellent", "good", "fair", "poor", "bad"]

SUBSET_MAP = {
    "distortion": "2k",
    "harmony": "7k",
    "layout": "6k",
    "lighting": "3k",
}

PROMPT1 = {
    "distortion": "<image>Please evaluate the spatial aesthetic distortion quality level of this image.",
    "harmony": "<image>Please evaluate the spatial aesthetic harmony quality level of this image.",
    "layout": "<image>Please evaluate the spatial aesthetic layout quality level of this image.",
    "lighting": "<image>Please evaluate the spatial aesthetic lighting quality level of this image.",
}


def calculate_iqa_score(logits: dict, item_image: str = "") -> float:
    """Convert class log-probabilities into a continuous score in [1, 5]."""
    safe_logits = {}
    for key in LABELS:
        if key not in logits:
            print(f"Warning: '{key}' not found in logits of {item_image}. Using fallback value.")
            safe_logits[key] = -50.0
        else:
            safe_logits[key] = logits[key]

    logprobs = np.array([safe_logits[k] for k in LABELS], dtype=np.float32)
    logprobs = logprobs - np.max(logprobs)
    probs = np.exp(logprobs) / np.sum(np.exp(logprobs))

    score_values = np.array([5, 4, 3, 2, 1], dtype=np.float32)
    return float(np.inner(probs, score_values))


def compute_plcc_srcc(csv_path: str, gt_column: str, pred_column: str = "score_pred") -> None:
    """Compute PLCC and SRCC."""
    df = pd.read_csv(csv_path)

    if gt_column not in df.columns:
        raise ValueError(f"Ground-truth column '{gt_column}' not found in {csv_path}")
    if pred_column not in df.columns:
        raise ValueError(f"Prediction column '{pred_column}' not found in {csv_path}")

    df = df.dropna(subset=[gt_column, pred_column])
    if len(df) == 0:
        raise ValueError("No valid rows available after dropping NaNs.")

    gt = df[gt_column]
    pred = df[pred_column]

    plcc_corr, _ = pearsonr(gt, pred)
    srcc_corr, _ = spearmanr(gt, pred)

    print(f"PLCC: {plcc_corr:.3f}")
    print(f"SRCC: {srcc_corr:.3f}")


def convert_logits_to_scores(input_jsonl: str, input_csv: str, output_csv: str) -> None:
    """Convert saved logits JSONL into continuous prediction scores and merge with CSV."""
    with open(input_jsonl, "r", encoding="utf-8") as f:
        data_list = [json.loads(line) for line in f if line.strip()]

    id_score_map = {}
    for item in data_list:
        item_image = item["images"][0]
        item_id = os.path.splitext(os.path.basename(item_image))[0]
        logits = item["logits"]
        score = calculate_iqa_score(logits, item_image)

        if str(item_id).isdigit():
            id_score_map[int(item_id)] = score
        else:
            id_score_map[str(item_id)] = score

    df = pd.read_csv(input_csv)
    if "id" not in df.columns:
        raise ValueError(f"'id' column not found in {input_csv}")

    df["score_pred"] = df["id"].map(id_score_map)

    output_dir = os.path.dirname(output_csv)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    df.to_csv(output_csv, index=False)
    print(f"Saved scored CSV to {output_csv}")


def extract_top_logprobs_as_dict(resp) -> dict:
    """
    Extract top logprobs for the rating token.

    Assumes the model output follows a template like:
    'The spatial aesthetic ... quality level of this image is good.'
    """
    content_logprobs = resp.choices[0].logprobs["content"]

    # Template-dependent heuristic from the original implementation.
    target_top_logprobs = content_logprobs[-3]["top_logprobs"]

    logits_dict = {}
    for entry in target_top_logprobs:
        token = entry["token"].strip().split(" ")[-1]
        logits_dict[token] = entry["logprob"]
    return logits_dict


def resolve_image_path(image_path: str, data_root: str) -> str:
    """
    Resolve image paths stored in JSONL.

    Supported cases:
    1. Absolute path -> return directly
    2. Path starts with 'SA-BENCH/' -> resolve relative to release root
    3. Other relative path -> resolve relative to data_root
    """
    if os.path.isabs(image_path):
        return image_path

    norm_path = os.path.normpath(image_path)
    data_root = os.path.abspath(data_root)

    if norm_path == "SA-BENCH" or norm_path.startswith(f"SA-BENCH{os.sep}"):
        release_root = os.path.dirname(data_root)
        return os.path.join(release_root, norm_path)

    return os.path.join(data_root, norm_path)


def run_inference(
    model_path: str,
    test_jsonl: str,
    output_jsonl: str,
    message_content: str,
    data_root: str,
    batch_size: int = 8,
    max_batch_size: int = 64,
) -> None:
    """Run SA-IQA inference and save top logprobs."""
    output_dir = os.path.dirname(output_jsonl)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(output_jsonl):
        print(f"{output_jsonl} already exists. Removing it.")
        os.remove(output_jsonl)

    engine = PtEngine(model_path, max_batch_size=max_batch_size)
    request_config = RequestConfig(
        max_tokens=2048,
        temperature=0,
        logprobs=True,
        top_logprobs=5,
    )

    message = {"role": "user", "content": message_content}

    infer_requests = []
    with open(test_jsonl, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            try:
                item = json.loads(line.strip())
                raw_image = item["images"][0]
                image = resolve_image_path(raw_image, data_root)

                if not os.path.exists(image):
                    raise FileNotFoundError(f"Image not found: {image}")

                infer_requests.append(InferRequest(messages=[message], images=[image]))
            except Exception as e:
                print(f"Error processing line {i}: {e}")

    batch_num = math.ceil(len(infer_requests) / batch_size)
    for batch_start in progress_iter(
        range(0, len(infer_requests), batch_size),
        desc=f"Evaluating [{os.path.basename(test_jsonl)}]",
        total=batch_num,
    ):
        batch_requests = infer_requests[batch_start:batch_start + batch_size]
        resp_list = engine.infer(batch_requests, request_config)

        with open(output_jsonl, "a", encoding="utf-8") as wf:
            for req, resp in zip(batch_requests, resp_list):
                logits_dict = extract_top_logprobs_as_dict(resp)
                output = {
                    "images": req.images,
                    "logits": logits_dict,
                }
                json.dump(output, wf, ensure_ascii=False)
                wf.write("\n")

    print(f"Saved inference logits to {output_jsonl}")


def get_default_test_jsonl(data_root: str, dimension: str) -> str:
    subset = SUBSET_MAP[dimension]
    return os.path.join(
        data_root,
        "annotations",
        f"{dimension}_{subset}_test_prompt1.jsonl",
    )


def get_default_input_csv(data_root: str, dimension: str) -> str:
    subset = SUBSET_MAP[dimension]
    return os.path.join(
        data_root,
        "annotations",
        f"{dimension}_{subset}_test.csv",
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Inference and evaluation script for SA-IQA prompt1.")

    parser.add_argument(
        "--mode",
        type=str,
        default="all",
        choices=["infer", "score", "eval", "all"],
        help="Run inference, score conversion, evaluation, or all stages.",
    )
    parser.add_argument(
        "--model_path",
        type=str,
        default="../../SA-IQA-model/sa-iqa-prompt1",
        help="Path to the trained SA-IQA prompt1 model.",
    )
    parser.add_argument(
        "--data_root",
        type=str,
        default="../../SA-BENCH",
        help="Path to the SA-BENCH dataset root.",
    )
    parser.add_argument(
        "--dimension",
        type=str,
        required=True,
        choices=["distortion", "harmony", "layout", "lighting"],
        help="Evaluation dimension.",
    )
    parser.add_argument(
        "--test_jsonl",
        type=str,
        default=None,
        help="Optional manual path to the test JSONL file.",
    )
    parser.add_argument(
        "--input_csv",
        type=str,
        default=None,
        help="Optional manual path to the test CSV file.",
    )
    parser.add_argument(
        "--output_jsonl",
        type=str,
        default=None,
        help="Optional manual path to save inference logits JSONL.",
    )
    parser.add_argument(
        "--output_csv",
        type=str,
        default=None,
        help="Optional manual path to save scored CSV.",
    )
    parser.add_argument(
        "--results_dir",
        type=str,
        default="../results",
        help="Directory to save results.",
    )
    parser.add_argument(
        "--gt_column",
        type=str,
        default=None,
        help="Ground-truth MOS column name. Defaults to '{dimension}_score_mos'.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=8,
        help="Batch size for inference.",
    )
    parser.add_argument(
        "--max_batch_size",
        type=int,
        default=64,
        help="Max batch size for PtEngine.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    message_content = PROMPT1[args.dimension]
    test_jsonl = args.test_jsonl or get_default_test_jsonl(args.data_root, args.dimension)
    input_csv = args.input_csv or get_default_input_csv(args.data_root, args.dimension)

    model_name = os.path.basename(os.path.normpath(args.model_path))
    result_stem = f"{args.dimension}_prompt1_{model_name}"

    output_jsonl = args.output_jsonl or os.path.join(args.results_dir, f"{result_stem}.jsonl")
    output_csv = args.output_csv or os.path.join(args.results_dir, f"{result_stem}.csv")
    gt_column = args.gt_column or f"{args.dimension}_score_mos"

    print(f"mode: {args.mode}")
    print(f"model_path: {args.model_path}")
    print(f"data_root: {args.data_root}")
    print(f"dimension: {args.dimension}")
    print(f"test_jsonl: {test_jsonl}")
    print(f"input_csv: {input_csv}")
    print(f"output_jsonl: {output_jsonl}")
    print(f"output_csv: {output_csv}")
    print(f"gt_column: {gt_column}")

    if args.mode in ["infer", "all"]:
        run_inference(
            model_path=args.model_path,
            test_jsonl=test_jsonl,
            output_jsonl=output_jsonl,
            message_content=message_content,
            data_root=args.data_root,
            batch_size=args.batch_size,
            max_batch_size=args.max_batch_size,
        )

    if args.mode in ["score", "all"]:
        convert_logits_to_scores(
            input_jsonl=output_jsonl,
            input_csv=input_csv,
            output_csv=output_csv,
        )

    if args.mode in ["eval", "all"]:
        compute_plcc_srcc(
            csv_path=output_csv,
            gt_column=gt_column,
            pred_column="score_pred",
        )


if __name__ == "__main__":
    main()


# Example usage:
#
# Run from SA-IQA/tools:
#   python infer_prompt1.py --mode all --dimension lighting
#
# Full pipeline for each dimension:
#   python infer_prompt1.py --mode all --dimension distortion
#   python infer_prompt1.py --mode all --dimension harmony
#   python infer_prompt1.py --mode all --dimension layout
#   python infer_prompt1.py --mode all --dimension lighting
#
# Inference only:
#   python infer_prompt1.py --mode infer --dimension lighting
#
# Score conversion only:
#   python infer_prompt1.py --mode score --dimension lighting
#
# Evaluation only:
#   python infer_prompt1.py --mode eval --dimension lighting
#
# Explicitly specify model/data/results paths:
#   python infer_prompt1.py \
#       --mode all \
#       --dimension lighting \
#       --model_path ../../SA-IQA-model/sa-iqa-prompt1 \
#       --data_root ../../SA-BENCH \
#       --results_dir ../results
#
# Run from the project root:
#   python SA-IQA/tools/infer_prompt1.py \
#       --mode all \
#       --dimension lighting \
#       --model_path ./SA-IQA-model/sa-iqa-prompt1 \
#       --data_root ./SA-BENCH \
#       --results_dir ./SA-IQA/results
#
# Manually specify input/output files:
#   python infer_prompt1.py \
#       --mode all \
#       --dimension lighting \
#       --test_jsonl ../../SA-BENCH/annotations/lighting_3k_test_prompt1.jsonl \
#       --input_csv ../../SA-BENCH/annotations/lighting_3k_test.csv \
#       --output_jsonl ../results/lighting_prompt1_sa-iqa-prompt1.jsonl \
#       --output_csv ../results/lighting_prompt1_sa-iqa-prompt1.csv
