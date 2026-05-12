from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

Token = Tuple[str, str, str, str]  # (word, chunk_outer, chunk_inner, clause)
Sentence = List[Token]


@dataclass
class DatasetStats:
    sentence_count: int
    token_count: int
    label_counts: dict[str, int]


def read_conll(path: str | Path) -> list[Sentence]:
    """Read CoNLL files with flat or extended chunk columns.

    Supported token lines:
    ID<TAB>FORM<TAB>CHUNK
    ID<TAB>FORM<TAB>CHUNK-OUTER<TAB>CHUNK-INNER<TAB>CLAUSE

    Lines beginning with '#' are ignored. Empty lines separate sentences.
    Three-column files are upgraded with '_' and 'O' defaults for the
    optional inner chunk and clause columns.
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
        if len(parts) not in {3, 5}:
            # tolerate whitespace-separated lines if needed
            parts = line.split()
        if len(parts) not in {3, 5}:
            raise ValueError(f"Invalid CoNLL line {line_no}: {raw_line!r}")

        word = parts[1]
        outer = parts[2]
        inner = parts[3] if len(parts) == 5 else "_"
        clause = parts[4] if len(parts) == 5 else "O"
        current.append((word, outer, inner, clause))

    if current:
        sentences.append(current)
    return sentences


def write_conll(sentences: Iterable[Sentence], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    chunks = []
    for sent in sentences:
        text = " ".join(word for word, _, _, _ in sent)
        chunks.append(f"# text = {text}")
        chunks.append("# columns = ID FORM CHUNK-OUTER CHUNK-INNER CLAUSE")
        for idx, (word, outer, inner, clause) in enumerate(sent, start=1):
            chunks.append(f"{idx}\t{word}\t{outer}\t{inner}\t{clause}")
        chunks.append("")
    path.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")


def dataset_stats(sentences: list[Sentence]) -> DatasetStats:
    counts: dict[str, int] = {}
    total = 0
    for sent in sentences:
        for _, outer, _, _ in sent:
            counts[outer] = counts.get(outer, 0) + 1
            total += 1
    return DatasetStats(sentence_count=len(sentences), token_count=total, label_counts=dict(sorted(counts.items())))
