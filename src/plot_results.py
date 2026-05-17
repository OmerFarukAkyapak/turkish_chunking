from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


METRIC_KEYS = ["accuracy", "weighted_precision", "weighted_recall", "weighted_f1"]
METRIC_LABELS = ["Accuracy", "Precision", "Recall", "F1-score"]


def parse_classification_report(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) != 5:
            continue
        label = parts[0]
        if label in {"accuracy", "macro", "weighted"}:
            continue
        try:
            rows.append(
                {
                    "label": label,
                    "precision": float(parts[1]),
                    "recall": float(parts[2]),
                    "f1": float(parts[3]),
                    "support": int(parts[4]),
                }
            )
        except ValueError:
            continue
    return rows


def style_axes(ax, title: str, ylabel: str = "Score") -> None:
    ax.set_title(title, fontsize=13, pad=12)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 1.05)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_per_class_metrics(results_dir: Path) -> None:
    rows = parse_classification_report(results_dir / "classification_report.txt")
    labels = [row["label"] for row in rows]
    precision = [row["precision"] for row in rows]
    recall = [row["recall"] for row in rows]
    f1 = [row["f1"] for row in rows]

    x = np.arange(len(labels))
    width = 0.24

    fig, ax = plt.subplots(figsize=(12, 6.5))
    fig.patch.set_facecolor("white")
    ax.bar(x - width, precision, width, label="Precision", color="#2f6f9f")
    ax.bar(x, recall, width, label="Recall", color="#d08c2f")
    ax.bar(x + width, f1, width, label="F1-score", color="#4f8f5f")

    style_axes(ax, "Per-Class Chunking Metrics")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(results_dir / "per_class_metrics.png", dpi=200)
    plt.close(fig)


def save_cross_validation_scores(results_dir: Path) -> None:
    data = json.loads((results_dir / "cross_validation_results.json").read_text(encoding="utf-8"))
    folds = data["folds"]
    fold_labels = [f"Fold {fold['fold']}" for fold in folds]
    accuracy = [fold["accuracy"] for fold in folds]
    f1 = [fold["weighted_f1"] for fold in folds]
    avg_accuracy = data["average"]["accuracy"]
    avg_f1 = data["average"]["weighted_f1"]

    x = np.arange(len(fold_labels))

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor("white")
    ax.plot(x, accuracy, marker="o", linewidth=2.5, label="Accuracy", color="#2f6f9f")
    ax.plot(x, f1, marker="s", linewidth=2.5, label="Weighted F1", color="#4f8f5f")
    ax.axhline(avg_accuracy, color="#2f6f9f", linestyle="--", alpha=0.45, linewidth=1.5)
    ax.axhline(avg_f1, color="#4f8f5f", linestyle="--", alpha=0.45, linewidth=1.5)

    style_axes(ax, "5-Fold Cross-Validation Scores")
    ax.set_xticks(x)
    ax.set_xticklabels(fold_labels)
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(results_dir / "cross_validation_scores.png", dpi=200)
    plt.close(fig)


def save_column_metrics_comparison(results_dir: Path) -> None:
    data = json.loads((results_dir / "metrics.json").read_text(encoding="utf-8"))
    columns = data["columns"]
    column_names = ["outer", "inner", "clause"]
    x = np.arange(len(column_names))
    width = 0.18

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor("white")
    colors = ["#2f6f9f", "#d08c2f", "#4f8f5f", "#8b5c9e"]

    for idx, (metric_key, metric_label) in enumerate(zip(METRIC_KEYS, METRIC_LABELS)):
        values = [columns[column][metric_key] for column in column_names]
        ax.bar(x + (idx - 1.5) * width, values, width, label=metric_label, color=colors[idx])

    style_axes(ax, "Column-Level Metrics Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(["Outer chunks", "Inner chunks", "Clauses"])
    ax.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    fig.savefig(results_dir / "column_metrics_comparison.png", dpi=200)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    save_per_class_metrics(results_dir)
    save_cross_validation_scores(results_dir)
    save_column_metrics_comparison(results_dir)

    print("Saved:")
    print(results_dir / "per_class_metrics.png")
    print(results_dir / "cross_validation_scores.png")
    print(results_dir / "column_metrics_comparison.png")


if __name__ == "__main__":
    main()
