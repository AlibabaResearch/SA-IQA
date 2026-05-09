import argparse
import json
import os
import pandas as pd


MOS_TO_WORD = {
    1: "bad",
    2: "poor",
    3: "fair",
    4: "good",
    5: "excellent",
}


PROMPTS = {
    "distortion": {
        4: (
            "<image><distortion>Please evaluate the spatial aesthetic distortion quality "
            "level of this image. The distortion dimension assesses whether soft furnishings "
            "(e.g., cabinets, carpets) or fixed structures (e.g., floors, walls) appear "
            "deformed or misaligned. Additionally, evaluate the realism and material accuracy "
            "of textures, and judge whether any distortion negatively impacts the overall "
            "aesthetic quality of the image."
        )
    }
}


RESPONSE_TEMPLATES = {
    "distortion": "The spatial aesthetic distortion quality level of this image is {rating}.",
}


def convert_csv_to_jsonl(
    input_csv: str,
    output_jsonl: str,
    image_dir: str,
    score_column: str,
    dimension: str,
    prompt_version: int,
):
    if dimension not in PROMPTS:
        raise ValueError(f"Unsupported dimension: {dimension}")

    if prompt_version not in PROMPTS[dimension]:
        raise ValueError(f"Unsupported prompt version {prompt_version} for dimension {dimension}")

    query = PROMPTS[dimension][prompt_version]
    response_template = RESPONSE_TEMPLATES[dimension]

    df = pd.read_csv(input_csv)

    if "id" not in df.columns:
        raise ValueError("Input CSV must contain an 'id' column.")
    if score_column not in df.columns:
        raise ValueError(f"Input CSV must contain the score column: {score_column}")

    num_written = 0
    with open(output_jsonl, "w", encoding="utf-8") as f_out:
        for _, row in df.iterrows():
            image_id = row["id"]

            if pd.isna(image_id):
                print("Skipping a row with empty image id.")
                continue

            score = row[score_column]
            if pd.isna(score):
                print(f"Skipping image {image_id}: empty score.")
                continue

            score = int(score)
            if score not in MOS_TO_WORD:
                print(f"Skipping image {image_id}: invalid score {score}.")
                continue

            rating_word = MOS_TO_WORD[score]
            response = response_template.format(rating=rating_word)
            image_path = os.path.join(image_dir, f"{image_id}.jpg")

            json_item = {
                "query": query,
                "response": response,
                "images": [image_path],
            }

            f_out.write(json.dumps(json_item, ensure_ascii=False) + "\n")
            num_written += 1

    print(f"Saved {num_written} samples to {output_jsonl}")


def parse_args():
    parser = argparse.ArgumentParser(description="Convert SA-BENCH annotation CSV to JSONL format.")
    parser.add_argument("--input_csv", type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument("--output_jsonl", type=str, required=True, help="Path to the output JSONL file.")
    parser.add_argument("--image_dir", type=str, required=True, help="Directory containing image files.")
    parser.add_argument("--score_column", type=str, required=True, help="Name of the score column in the CSV.")
    parser.add_argument(
        "--dimension",
        type=str,
        required=True,
        choices=["distortion"],
        help="Evaluation dimension.",
    )
    parser.add_argument(
        "--prompt_version",
        type=int,
        default=4,
        help="Prompt version to use.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    convert_csv_to_jsonl(
        input_csv=args.input_csv,
        output_jsonl=args.output_jsonl,
        image_dir=args.image_dir,
        score_column=args.score_column,
        dimension=args.dimension,
        prompt_version=args.prompt_version,
    )
