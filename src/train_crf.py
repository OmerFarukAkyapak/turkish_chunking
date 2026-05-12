from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import sklearn_crfsuite
from sklearn_crfsuite import metrics as crf_metrics

from data_utils import read_conll
from features import sent2features, sent2labels


def flatten(nested):
    return [item for seq in nested for item in seq]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="dataset/processed/train.conll")
    parser.add_argument("--test", default="dataset/processed/test.conll")
    parser.add_argument("--model-out", default="results/chunking_crf_model.pkl")
    parser.add_argument("--results-dir", default="results")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    train_sents = read_conll(args.train)
    test_sents = read_conll(args.test)

    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]
    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    crf = sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True,
    )
    crf.fit(X_train, y_train)
    y_pred = crf.predict(X_test)

    labels = sorted(crf.classes_)
    flat_true = flatten(y_test)
    flat_pred = flatten(y_pred)

    acc = accuracy_score(flat_true, flat_pred)
    report = classification_report(flat_true, flat_pred, labels=labels, digits=4, zero_division=0)

    # Entity-level sequence metrics are also useful for chunking.
    flat_f1 = crf_metrics.flat_f1_score(y_test, y_pred, average="weighted", labels=labels)
    flat_precision = crf_metrics.flat_precision_score(y_test, y_pred, average="weighted", labels=labels, zero_division=0)
    flat_recall = crf_metrics.flat_recall_score(y_test, y_pred, average="weighted", labels=labels, zero_division=0)

    metrics = {
        "accuracy": acc,
        "weighted_precision": flat_precision,
        "weighted_recall": flat_recall,
        "weighted_f1": flat_f1,
        "train_sentence_count": len(train_sents),
        "test_sentence_count": len(test_sents),
    }

    (results_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    (results_dir / "classification_report.txt").write_text(report, encoding="utf-8")

    cm = confusion_matrix(flat_true, flat_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(12, 10))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, xticks_rotation=45, values_format="d")
    ax.set_title("Chunking Confusion Matrix")
    fig.tight_layout()
    fig.savefig(results_dir / "confusion_matrix.png", dpi=200)
    plt.close(fig)

    with open(args.model_out, "wb") as f:
        pickle.dump(crf, f)

    print("Training complete.")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
