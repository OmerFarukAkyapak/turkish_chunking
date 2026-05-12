from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import sklearn_crfsuite
from sklearn_crfsuite import metrics as crf_metrics

from data_utils import read_conll
from features import sent2features, sent2labels


def flatten(nested):
    return [item for seq in nested for item in seq]


def make_crf() -> sklearn_crfsuite.CRF:
    return sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True,
    )


def train_column(X_train, train_sents, X_test, test_sents, column: str) -> tuple[sklearn_crfsuite.CRF, dict, str, list, list, list[str]]:
    y_train = [sent2labels(s, column=column) for s in train_sents]
    y_test = [sent2labels(s, column=column) for s in test_sents]

    crf = make_crf()
    crf.fit(X_train, y_train)
    y_pred = crf.predict(X_test)

    labels = sorted(crf.classes_)
    flat_true = flatten(y_test)
    flat_pred = flatten(y_pred)

    metrics = {
        "accuracy": accuracy_score(flat_true, flat_pred),
        "weighted_precision": crf_metrics.flat_precision_score(y_test, y_pred, average="weighted", labels=labels, zero_division=0),
        "weighted_recall": crf_metrics.flat_recall_score(y_test, y_pred, average="weighted", labels=labels, zero_division=0),
        "weighted_f1": crf_metrics.flat_f1_score(y_test, y_pred, average="weighted", labels=labels),
    }
    report = classification_report(flat_true, flat_pred, labels=labels, digits=4, zero_division=0)
    return crf, metrics, report, y_test, y_pred, labels


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
    X_test = [sent2features(s) for s in test_sents]

    models = {}
    column_results = {}
    reports = {}
    predictions = {}

    for column in ["outer", "inner", "clause"]:
        crf, column_metrics, report, y_test, y_pred, labels = train_column(
            X_train, train_sents, X_test, test_sents, column
        )
        models[column] = crf
        column_results[column] = column_metrics
        reports[column] = report
        predictions[column] = (y_test, y_pred, labels)

    metrics = {
        **column_results["outer"],
        "train_sentence_count": len(train_sents),
        "test_sentence_count": len(test_sents),
        "columns": column_results,
    }

    (results_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    (results_dir / "classification_report.txt").write_text(reports["outer"], encoding="utf-8")
    (results_dir / "classification_report_inner.txt").write_text(reports["inner"], encoding="utf-8")
    (results_dir / "classification_report_clause.txt").write_text(reports["clause"], encoding="utf-8")

    y_test, y_pred, labels = predictions["outer"]
    flat_true = flatten(y_test)
    flat_pred = flatten(y_pred)
    cm = confusion_matrix(flat_true, flat_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    white_to_green = LinearSegmentedColormap.from_list("white_to_green", ["#ffffff", "#005a32"])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, cmap=white_to_green, xticks_rotation=45, values_format="d", colorbar=True)
    for text in disp.text_.ravel():
        text.set_color("black")
    if disp.im_.colorbar:
        disp.im_.colorbar.set_label("Token count")
    ax.set_title("Chunking Confusion Matrix (Counts)")
    fig.tight_layout()
    fig.savefig(results_dir / "confusion_matrix.png", dpi=200)
    plt.close(fig)

    with open(args.model_out, "wb") as f:
        pickle.dump(models, f)

    print("Training complete.")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
