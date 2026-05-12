from __future__ import annotations

import argparse
from pathlib import Path
from sklearn.model_selection import train_test_split

from data_utils import read_conll, write_conll, dataset_stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="dataset/processed/chunking_annotated.conll")
    parser.add_argument("--out-dir", default="dataset/processed")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    sentences = read_conll(args.input)
    train, test = train_test_split(sentences, test_size=args.test_size, random_state=args.seed)

    out = Path(args.out_dir)
    write_conll(train, out / "train.conll")
    write_conll(test, out / "test.conll")

    stats = dataset_stats(sentences)
    stats_text = [
        f"Sentence count: {stats.sentence_count}",
        f"Token count: {stats.token_count}",
        "",
        "Label distribution:",
    ]
    for label, count in stats.label_counts.items():
        stats_text.append(f"{label}\t{count}")
    (out / "dataset_stats.txt").write_text("\n".join(stats_text) + "\n", encoding="utf-8")
    print("Dataset prepared.")
    print("\n".join(stats_text))


if __name__ == "__main__":
    main()
