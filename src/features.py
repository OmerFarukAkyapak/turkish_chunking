from __future__ import annotations

from data_utils import Sentence


def word2features(sent: Sentence, i: int) -> dict:
    word = sent[i][0]
    lower = word.lower()

    features = {
        "bias": 1.0,
        "word.lower": lower,
        "word[-1:]": lower[-1:],
        "word[-2:]": lower[-2:],
        "word[-3:]": lower[-3:],
        "word[:1]": lower[:1],
        "word[:2]": lower[:2],
        "word.isupper": word.isupper(),
        "word.istitle": word.istitle(),
        "word.isdigit": word.isdigit(),
        "contains_apostrophe": "'" in word or "’" in word,
        "contains_hyphen": "-" in word,
    }

    if i > 0:
        prev = sent[i - 1][0]
        prev_lower = prev.lower()
        features.update({
            "-1:word.lower": prev_lower,
            "-1:word.istitle": prev.istitle(),
            "-1:word.isupper": prev.isupper(),
        })
    else:
        features["BOS"] = True

    if i < len(sent) - 1:
        nxt = sent[i + 1][0]
        nxt_lower = nxt.lower()
        features.update({
            "+1:word.lower": nxt_lower,
            "+1:word.istitle": nxt.istitle(),
            "+1:word.isupper": nxt.isupper(),
        })
    else:
        features["EOS"] = True

    return features


def sent2features(sent: Sentence) -> list[dict]:
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent: Sentence, column: str = "outer") -> list[str]:
    column_index = {"outer": 1, "inner": 2, "clause": 3}[column]
    return [token[column_index] for token in sent]


def sent2tokens(sent: Sentence) -> list[str]:
    return [word for word, _, _, _ in sent]
