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
    dummy_sent = [(tok, "O") for tok in tokens]
    pred = model.predict_single(sent2features(dummy_sent))

    print(f"# text = {args.text}")
    for i, (tok, label) in enumerate(zip(tokens, pred), start=1):
        print(f"{i}\t{tok}\t{label}")


if __name__ == "__main__":
    main()
