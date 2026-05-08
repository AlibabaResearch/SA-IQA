import argparse
import json
import os

import numpy as np

from swift.llm import PtEngine, RequestConfig, InferRequest


LABELS = ["excellent", "good", "fair", "poor", "bad"]
SCORE_VALUES = np.array([5, 4, 3, 2, 1], dtype=np.float32)
DIMENSIONS = ["distortion", "harmony", "layout", "lighting"]

PROMPTS = {
    "distortion": (
        "<image><distortion>Please evaluate the spatial aesthetic distortion quality level of this image. "
        "The distortion dimension assesses whether soft furnishings (e.g., cabinets, carpets) or fixed "
        "structures (e.g., floors, walls) appear deformed or misaligned. Additionally, evaluate the realism "
        "and material accuracy of textures, and judge whether any distortion negatively impacts the overall "
        "aesthetic quality of the image."
    ),
    "harmony": (
        "<image><harmony>Please evaluate the spatial aesthetic harmony quality level of this image. "
        "The harmony dimension focuses on stylistic consistency, color coordination, and overall visual cohesion. "
        "Examine how well the combination of elements creates a balanced and visually pleasant composition, "
        "avoiding clashes or imbalances in style and color."
    ),
    "layout": (
        "<image><layout>Please evaluate the spatial aesthetic layout quality level of this image. "
        "The layout dimension describes the spatial distribution, positional relationships, and quantity of major "
        "elements within the space. Consider how the layout supports the overall visual order, maintains balance, "
        "and enhances the functional aesthetics of the image."
    ),
    "lighting": (
        "<image><lighting>Please evaluate the spatial aesthetic lighting quality level of this image. "
        "The lighting dimension examines the quality of light effects, shadow interactions, and the realism of "
        "light sources. Assess how well lighting contributes to the overall depth, mood, and authenticity of the "
        "image, emphasizing both natural and artificial lighting scenarios."
    ),
}


def extract_top_logprobs_as_dict(resp) -> dict:
    content_logprobs = resp.choices[0].logprobs["content"]
    target_top_logprobs = content_logprobs[-3]["top_logprobs"]

    logits_dict = {}
    for entry in target_top_logprobs:
        token = entry["token"].strip().split(" ")[-1]
        logits_dict[token] = entry["logprob"]
    return logits_dict


def calculate_iqa_score(logits: dict) -> tuple[float, dict, list]:
    safe_logits = {}
    missing_labels = []

    for key in LABELS:
        if key not in logits:
            safe_logits[key] = -50.0
            missing_labels.append(key)
        else:
            safe_logits[key] = logits[key]

    logprobs = np.array([safe_logits[k] for k in LABELS], dtype=np.float32)
    logprobs = logprobs - np.max(logprobs)
    probs = np.exp(logprobs) / np.sum(np.exp(logprobs))

    score = float(np.inner(probs, SCORE_VALUES))
    prob_dict = {label: float(prob) for label, prob in zip(LABELS, probs)}
    return score, prob_dict, missing_labels


def build_engine(model_path: str, max_batch_size: int):
    return PtEngine(model_path, max_batch_size=max_batch_size)


def build_request_config():
    return RequestConfig(
        max_tokens=2048,
        temperature=0,
        logprobs=True,
        top_logprobs=5,
    )


def infer_single_dimension(engine, request_config, image_path: str, dimension: str) -> dict:
    message = {"role": "user", "content": PROMPTS[dimension]}
    req = InferRequest(messages=[message], images=[image_path])
    resp = engine.infer([req], request_config)[0]

    logits = extract_top_logprobs_as_dict(resp)
    score, probs, missing_labels = calculate_iqa_score(logits)

    return {
        "dimension": dimension,
        "score": score,
        "logits": logits,
        "probs": probs,
        "missing_labels": missing_labels,
        "response_text": resp.choices[0].message.content,
    }


def print_dimension_result(result: dict) -> None:
    print(f"[{result['dimension']}]")
    print(f"score: {result['score']:.4f}")
    print(f"response: {result['response_text']}")
    print("label probabilities:")
    for label in LABELS:
        print(f"  - {label}: {result['probs'][label]:.6f}")
    if result["missing_labels"]:
        print(f"missing labels in top_logprobs (fallback used): {', '.join(result['missing_labels'])}")
    print()


def parse_args():
    parser = argparse.ArgumentParser(description="Single-image inference for SA-IQA prompt4.")

    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to the input image.",
    )
    parser.add_argument(
        "--dimension",
        type=str,
        default="all",
        choices=["distortion", "harmony", "layout", "lighting", "all"],
        help="Target dimension to evaluate, or 'all' for all four dimensions plus average score.",
    )
    parser.add_argument(
        "--model_path",
        type=str,
        default="../../SA-IQA-model/sa-iqa-prompt4",
        help="Path to the trained SA-IQA prompt4 model.",
    )
    parser.add_argument(
        "--max_batch_size",
        type=int,
        default=4,
        help="Max batch size for PtEngine.",
    )
    parser.add_argument(
        "--save_json",
        type=str,
        default=None,
        help="Optional path to save inference results as JSON.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    image_path = os.path.abspath(args.image)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    print(f"image: {image_path}")
    print(f"model_path: {args.model_path}")
    print(f"dimension: {args.dimension}")

    engine = build_engine(args.model_path, args.max_batch_size)
    request_config = build_request_config()

    if args.dimension == "all":
        results = []
        for dimension in DIMENSIONS:
            result = infer_single_dimension(engine, request_config, image_path, dimension)
            results.append(result)
            print_dimension_result(result)

        score_summary = {item["dimension"]: item["score"] for item in results}
        overall_score = float(np.mean([item["score"] for item in results]))

        print("[summary]")
        for dimension in DIMENSIONS:
            print(f"{dimension}: {score_summary[dimension]:.4f}")
        print(f"overall_score: {overall_score:.4f}")

        output = {
            "image": image_path,
            "model_path": args.model_path,
            "mode": "all",
            "results": results,
            "overall_score": overall_score,
        }
    else:
        result = infer_single_dimension(engine, request_config, image_path, args.dimension)
        print_dimension_result(result)

        output = {
            "image": image_path,
            "model_path": args.model_path,
            "mode": "single",
            "results": [result],
        }

    if args.save_json is not None:
        output_dir = os.path.dirname(args.save_json)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(args.save_json, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Saved results to {args.save_json}")


if __name__ == "__main__":
    main()


# Example usage:
#
# Run from SA-IQA/tools:
#   python infer_single_image_prompt4.py --image /path/to/image.jpg --dimension lighting
#
# Evaluate all four dimensions and output average score:
#   python infer_single_image_prompt4.py --image /path/to/image.jpg --dimension all
#
# Specify model path explicitly:
#   python infer_single_image_prompt4.py \
#       --image /path/to/image.jpg \
#       --dimension all \
#       --model_path ../../SA-IQA-model/sa-iqa-prompt4
#
# Save results to JSON:
#   python infer_single_image_prompt4.py \
#       --image /path/to/image.jpg \
#       --dimension all \
#       --save_json ../results/single_image_result.json

# python infer_single_image_prompt4.py --image ../../SA-BENCH/images/distortion/images/distortion_214.jpg --dimension all
