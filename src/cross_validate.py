from __future__ import annotations

import argparse
import json
from pathlib import Path

import sklearn_crfsuite
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn_crfsuite import metrics as crf_metrics

from data_utils import read_conll
from features import sent2features, sent2labels


def flatten(nested):
    return [item for seq in nested for item in seq]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="dataset/processed/chunking_annotated.conll")
    parser.add_argument("--folds", type=int, default=5)
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    out = Path(args.results_dir)
    out.mkdir(parents=True, exist_ok=True)

    sentences = read_conll(args.input)
    X = [sent2features(s) for s in sentences]
    y = [sent2labels(s) for s in sentences]

    kf = KFold(n_splits=args.folds, shuffle=True, random_state=args.seed)
    fold_results = []

    for fold, (train_idx, test_idx) in enumerate(kf.split(X), start=1):
        X_train = [X[i] for i in train_idx]
        y_train = [y[i] for i in train_idx]
        X_test = [X[i] for i in test_idx]
        y_test = [y[i] for i in test_idx]

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

        result = {
            "fold": fold,
            "accuracy": accuracy_score(flatten(y_test), flatten(y_pred)),
            "weighted_precision": crf_metrics.flat_precision_score(y_test, y_pred, average="weighted", labels=labels, zero_division=0),
            "weighted_recall": crf_metrics.flat_recall_score(y_test, y_pred, average="weighted", labels=labels, zero_division=0),
            "weighted_f1": crf_metrics.flat_f1_score(y_test, y_pred, average="weighted", labels=labels),
            "train_sentence_count": len(train_idx),
            "test_sentence_count": len(test_idx),
        }
        fold_results.append(result)
        print(result)

    avg = {
        key: sum(r[key] for r in fold_results) / len(fold_results)
        for key in ["accuracy", "weighted_precision", "weighted_recall", "weighted_f1"]
    }
    output = {"folds": fold_results, "average": avg}
    (out / "cross_validation_results.json").write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Average:", avg)


if __name__ == "__main__":
    main()
