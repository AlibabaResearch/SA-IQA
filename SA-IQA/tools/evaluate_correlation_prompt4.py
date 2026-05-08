import argparse
import os

import pandas as pd
from scipy.stats import pearsonr, spearmanr


DIMENSIONS = ["distortion", "harmony", "layout", "lighting"]


def load_and_merge_csv_files(results_dir: str, prompt_version: int, model_name: str) -> pd.DataFrame:
    merged_df_list = []

    for dimension in DIMENSIONS:
        csv_path = os.path.join(
            results_dir,
            f"{dimension}_prompt{prompt_version}_{model_name}.csv"
        )

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Result file not found: {csv_path}")

        df = pd.read_csv(csv_path)

        gt_column = f"{dimension}_score_mos"
        pred_column = "score_pred"

        if "id" not in df.columns:
            raise ValueError(f"'id' column not found in {csv_path}")
        if gt_column not in df.columns:
            raise ValueError(f"'{gt_column}' column not found in {csv_path}")
        if pred_column not in df.columns:
            raise ValueError(f"'{pred_column}' column not found in {csv_path}")

        temp_df = pd.DataFrame({
            "dimension": dimension,
            "id": df["id"],
            "score_mos": df[gt_column],
            "score_pred": df[pred_column],
        })

        merged_df_list.append(temp_df)

    final_df = pd.concat(merged_df_list, ignore_index=True)
    return final_df


def compute_plcc_srcc(df: pd.DataFrame) -> tuple:
    score_mos = pd.to_numeric(df["score_mos"], errors="coerce")
    score_pred = pd.to_numeric(df["score_pred"], errors="coerce")

    valid_mask = score_mos.notna() & score_pred.notna()
    score_mos = score_mos[valid_mask]
    score_pred = score_pred[valid_mask]

    if len(score_mos) == 0:
        raise ValueError("No valid rows available for correlation calculation.")

    plcc_value, _ = pearsonr(score_mos, score_pred)
    srcc_value, _ = spearmanr(score_mos, score_pred)

    return plcc_value, srcc_value


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate overall PLCC/SRCC for SA-IQA prompt4 results.")
    parser.add_argument(
        "--results_dir",
        type=str,
        default="../results",
        help="Directory containing per-dimension scored CSV files.",
    )
    parser.add_argument(
        "--output_csv",
        type=str,
        default=None,
        help="Path to save merged CSV. Defaults to ../results/all_prompt4_sa-iqa-prompt4.csv",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="sa-iqa-prompt4",
        help="Model name suffix used in result CSV filenames.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    prompt_version = 4

    final_df = load_and_merge_csv_files(
        results_dir=args.results_dir,
        prompt_version=prompt_version,
        model_name=args.model_name,
    )

    output_csv = args.output_csv or os.path.join(
        args.results_dir,
        f"all_prompt{prompt_version}_{args.model_name}.csv"
    )

    output_dir = os.path.dirname(output_csv)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    final_df.to_csv(output_csv, index=False)
    print(f"Merged CSV saved to: {output_csv}")

    plcc_value, srcc_value = compute_plcc_srcc(final_df)

    print(f"PLCC: {plcc_value:.3f}")
    print(f"SRCC: {srcc_value:.3f}")


if __name__ == "__main__":
    main()


# Example usage:
#
# Run from SA-IQA/tools:
#   python evaluate_correlation_prompt4.py
#
# Specify results directory explicitly:
#   python evaluate_correlation_prompt4.py \
#       --results_dir ../results
#
# Specify output CSV explicitly:
#   python evaluate_correlation_prompt4.py \
#       --results_dir ../results \
#       --output_csv ../results/all_prompt4_sa-iqa-prompt4.csv
#
# Run from the project root:
#   python SA-IQA/tools/evaluate_correlation_prompt4.py \
#       --results_dir ./SA-IQA/results
