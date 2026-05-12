from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

Token = Tuple[str, str]  # (word, chunk_label)
Sentence = List[Token]


@dataclass
class DatasetStats:
    sentence_count: int
    token_count: int
    label_counts: dict[str, int]


def read_conll(path: str | Path) -> list[Sentence]:
    """Read CoNLL file with lines: ID<TAB>FORM<TAB>CHUNK.

    Lines beginning with '# text =' are ignored. Empty lines separate sentences.
    """
    path = Path(path)
    sentences: list[Sentence] = []
    current: Sentence = []

    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            if current:
                sentences.append(current)
                current = []
            continue
        if line.startswith("#"):
            continue

        parts = line.split("\t")
        if len(parts) != 3:
            # tolerate whitespace-separated lines if needed
            parts = line.split()
        if len(parts) < 3:
            raise ValueError(f"Invalid CoNLL line {line_no}: {raw_line!r}")

        word = parts[1]
        label = parts[-1]
        current.append((word, label))

    if current:
        sentences.append(current)
    return sentences


def write_conll(sentences: Iterable[Sentence], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    chunks = []
    for sent in sentences:
        text = " ".join(word for word, _ in sent)
        chunks.append(f"# text = {text}")
        for idx, (word, label) in enumerate(sent, start=1):
            chunks.append(f"{idx}\t{word}\t{label}")
        chunks.append("")
    path.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")


def dataset_stats(sentences: list[Sentence]) -> DatasetStats:
    counts: dict[str, int] = {}
    total = 0
    for sent in sentences:
        for _, label in sent:
            counts[label] = counts.get(label, 0) + 1
            total += 1
    return DatasetStats(sentence_count=len(sentences), token_count=total, label_counts=dict(sorted(counts.items())))
