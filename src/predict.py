from __future__ import annotations

import argparse
import pickle
import re

from features import sent2features


def simple_tokenize(text: str) -> list[str]:
    return re.findall(r"\w+(?:['’]\w+)?|[^\w\s]", text, flags=re.UNICODE)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="results/chunking_crf_model.pkl")
    parser.add_argument("--text", required=True)
    args = parser.parse_args()

    with open(args.model, "rb") as f:
        model = pickle.load(f)

    tokens = simple_tokenize(args.text)
    dummy_sent = [(tok, "O", "_", "O") for tok in tokens]
    features = sent2features(dummy_sent)
    if isinstance(model, dict):
        pred_outer = model["outer"].predict_single(features)
        pred_inner = model["inner"].predict_single(features)
        pred_clause = model["clause"].predict_single(features)
    else:
        pred_outer = model.predict_single(features)
        pred_inner = ["_"] * len(tokens)
        pred_clause = ["O"] * len(tokens)

    print(f"# text = {args.text}")
    print("# columns = ID FORM CHUNK-OUTER CHUNK-INNER CLAUSE")
    for i, (tok, outer, inner, clause) in enumerate(zip(tokens, pred_outer, pred_inner, pred_clause), start=1):
        print(f"{i}\t{tok}\t{outer}\t{inner}\t{clause}")


if __name__ == "__main__":
    main()
