from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


TOKEN_RE = re.compile(r"\.{3}|\d+(?:[.,]\d+)?|\w+(?:['’]\w+)?|[^\w\s]", re.UNICODE)

PUNCT = {
    ".",
    ",",
    ";",
    ":",
    "!",
    "?",
    "...",
    '"',
    "'",
    "“",
    "”",
    "‘",
    "’",
    "(",
    ")",
    "[",
    "]",
}

CONJUNCTIONS = {
    "ama",
    "ancak",
    "ve",
    "veya",
    "ya",
    "yahut",
    "fakat",
    "çünkü",
    "ki",
    "ile",
    "hem",
    "de",
    "da",
}

ADVERBS = {
    "akşam",
    "ardından",
    "artık",
    "asla",
    "az",
    "bazen",
    "belki",
    "beraber",
    "birden",
    "birlikte",
    "böylece",
    "bugün",
    "çok",
    "daha",
    "daima",
    "derhal",
    "diye",
    "dün",
    "erken",
    "evvel",
    "gece",
    "geç",
    "gizlice",
    "gün",
    "gündüz",
    "güzelce",
    "hemen",
    "hep",
    "henüz",
    "hızla",
    "için",
    "iyice",
    "kaç",
    "kadar",
    "karşı",
    "mutlaka",
    "nasıl",
    "nihayet",
    "önce",
    "öyle",
    "sabah",
    "sakince",
    "sessizce",
    "sonra",
    "sürekli",
    "tekrar",
    "uzun",
    "yavaşça",
    "yine",
    "zaman",
}

ADJECTIVES = {
    "aç",
    "aydınlık",
    "büyük",
    "çaresiz",
    "eski",
    "eşsiz",
    "gizli",
    "güzel",
    "gururlu",
    "hüzünlü",
    "ihtiyar",
    "iyi",
    "kocaman",
    "küçük",
    "meraklı",
    "parlak",
    "sihirli",
    "sonsuz",
    "yaşlı",
    "yoksul",
}

LIGHT_VERB_NOUNS = {
    "devam",
    "dua",
    "fark",
    "haber",
    "karar",
    "rehberlik",
    "saygı",
    "selam",
    "teşekkür",
    "umut",
    "veda",
    "yardım",
}

VERB_ROOTS = {
    "al",
    "bak",
    "başla",
    "bekle",
    "bil",
    "bul",
    "çalış",
    "de",
    "dinle",
    "dolaş",
    "dur",
    "et",
    "gel",
    "git",
    "gör",
    "göster",
    "gül",
    "iste",
    "kal",
    "konuş",
    "ol",
    "otur",
    "söyle",
    "ver",
    "yap",
}

VERB_EXCEPTIONS = {
    "gümüş",
    "kuş",
    "yemiş",
}

FINITE_VERB_SUFFIXES = (
    "acağım",
    "eceğim",
    "acaktı",
    "ecekti",
    "acak",
    "ecek",
    "arım",
    "erim",
    "ırım",
    "irim",
    "urum",
    "ürüm",
    "ardı",
    "erdi",
    "ırdı",
    "irdi",
    "urdu",
    "ürdü",
    "dım",
    "dim",
    "dum",
    "düm",
    "tım",
    "tim",
    "tum",
    "tüm",
    "ıyor",
    "iyor",
    "uyor",
    "üyor",
    "mış",
    "miş",
    "muş",
    "müş",
    "dı",
    "di",
    "du",
    "dü",
    "tı",
    "ti",
    "tu",
    "tü",
    "malı",
    "meli",
    "sa",
    "se",
)

NONFINITE_VERB_SUFFIXES = (
    "mak",
    "mek",
    "maya",
    "meye",
    "mayı",
    "meyi",
    "ması",
    "mesi",
    "masını",
    "mesini",
    "dığı",
    "diği",
    "duğu",
    "düğü",
    "dığını",
    "diğini",
    "duğunu",
    "düğünü",
    "arak",
    "erek",
    "ınca",
    "ince",
    "unca",
    "ünce",
    "ıp",
    "ip",
    "up",
    "üp",
)

PARTICIPLE_SUFFIXES = (
    "dığı",
    "diği",
    "duğu",
    "düğü",
    "acağı",
    "eceği",
)

PARTICIPLE_WORDS = {
    "açılan",
    "alan",
    "bakan",
    "bulan",
    "çıkan",
    "eden",
    "geçen",
    "gelen",
    "giden",
    "olan",
    "söyleyen",
    "tutan",
    "yapan",
    "yanan",
}

COMPLEMENT_SUFFIXES = (
    "mak",
    "mek",
    "mayı",
    "meyi",
    "ması",
    "mesi",
    "masını",
    "mesini",
    "dığını",
    "diğini",
    "duğunu",
    "düğünü",
    "acağına",
    "eceğine",
)


@dataclass(frozen=True)
class AnnotatedToken:
    form: str
    outer: str
    inner: str = "_"
    clause: str = "O"


def tr_lower(text: str) -> str:
    return text.replace("I", "ı").replace("İ", "i").lower()


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text)


def read_raw_sentences(path: str | Path) -> list[str]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip().startswith("Etiketlenecek"))
    except StopIteration as exc:
        raise ValueError("Raw file does not contain an 'Etiketlenecek cümleler:' marker.") from exc
    return [line.strip() for line in lines[start + 1 :] if line.strip()]


def is_punctuation(token: str) -> bool:
    return token in PUNCT or all(ch in PUNCT for ch in token)


def is_verb_like(token: str) -> bool:
    lower = tr_lower(token)
    if lower in VERB_EXCEPTIONS:
        return False
    if lower in {"varmış", "yokmuş", "vardı", "yoktu"}:
        return True
    if lower.startswith(("et", "ol", "de")) and len(lower) > 2:
        return True
    if lower in VERB_ROOTS:
        return True
    return lower.endswith(FINITE_VERB_SUFFIXES) or lower.endswith(NONFINITE_VERB_SUFFIXES)


def is_participle(token: str) -> bool:
    lower = tr_lower(token)
    return lower in PARTICIPLE_WORDS or (lower not in VERB_EXCEPTIONS and lower.endswith(PARTICIPLE_SUFFIXES))


def is_complement_verb(token: str) -> bool:
    lower = tr_lower(token)
    return lower.endswith(COMPLEMENT_SUFFIXES)


def is_locative_like(token: str) -> bool:
    lower = tr_lower(token)
    return lower.endswith(("da", "de", "ta", "te", "nda", "nde", "ında", "inde", "unda", "ünde"))


def base_chunk_type(tokens: list[str], index: int) -> str:
    token = tokens[index]
    lower = tr_lower(token)
    next_lower = tr_lower(tokens[index + 1]) if index + 1 < len(tokens) else ""

    if is_punctuation(token):
        return "O"
    if is_participle(token) and next_lower and not is_punctuation(tokens[index + 1]):
        return "NP"
    if lower in LIGHT_VERB_NOUNS and is_verb_like(tokens[index + 1] if index + 1 < len(tokens) else ""):
        return "VP"
    if is_verb_like(token):
        return "VP"
    if lower in ADVERBS or lower.endswith(("ca", "ce", "ça", "çe")):
        return "ADVP"
    if lower in ADJECTIVES and (not next_lower or is_punctuation(tokens[index + 1])):
        return "ADJP"
    if lower in CONJUNCTIONS:
        return "CONJ"
    return "NP"


def outer_labels(tokens: list[str]) -> list[str]:
    chunk_types = [base_chunk_type(tokens, i) for i in range(len(tokens))]
    for i, chunk_type in enumerate(chunk_types):
        if chunk_type != "CONJ":
            continue
        prev_type = chunk_types[i - 1] if i > 0 else "O"
        next_type = chunk_types[i + 1] if i + 1 < len(chunk_types) else "O"
        chunk_types[i] = "NP" if prev_type == next_type == "NP" else "O"

    labels: list[str] = []
    prev_type = "O"
    for i, chunk_type in enumerate(chunk_types):
        if chunk_type == "O":
            labels.append("O")
        elif chunk_type == "NP" and i > 0 and is_locative_like(tokens[i]) and prev_type == "NP":
            labels.append("B-NP")
        elif chunk_type == "VP" and tr_lower(tokens[i]) in LIGHT_VERB_NOUNS:
            labels.append("B-VP")
        elif chunk_type == prev_type:
            labels.append(f"I-{chunk_type}")
        else:
            labels.append(f"B-{chunk_type}")
        prev_type = chunk_type
    return labels


def previous_boundary(tokens: list[str], index: int) -> int:
    boundary_words = CONJUNCTIONS | {"diye"}
    cursor = index
    while cursor > 0:
        prev = tokens[cursor - 1]
        if is_punctuation(prev) or tr_lower(prev) in boundary_words:
            break
        cursor -= 1
    return cursor


def complement_clause_start(tokens: list[str], index: int) -> int:
    start = previous_boundary(tokens, index)
    candidate = start
    for cursor in range(index - 1, start - 1, -1):
        lower = tr_lower(tokens[cursor])
        if is_punctuation(tokens[cursor]) or lower in CONJUNCTIONS:
            break
        if lower in ADVERBS or lower.endswith(("ca", "ce", "ça", "çe")) or is_locative_like(tokens[cursor]):
            candidate = cursor
    return candidate


def relative_clause_start(tokens: list[str], outers: list[str], index: int) -> int:
    start = previous_boundary(tokens, index)
    while start < index and outers[start].endswith("ADVP"):
        start += 1
    return start


def force_np_outer(outers: list[str], start: int, end: int) -> None:
    for pos in range(start, end + 1):
        outers[pos] = "B-NP" if pos == start else "I-NP"


def mark_span(values: list[str], start: int, end: int, label: str, empty_value: str) -> None:
    for pos in range(start, end + 1):
        values[pos] = f"B-{label}" if pos == start or values[pos] != empty_value else f"I-{label}"


def annotate_sentence(text: str) -> list[AnnotatedToken]:
    tokens = tokenize(text)
    outers = outer_labels(tokens)
    inners = ["_"] * len(tokens)
    clauses = ["O"] * len(tokens)

    for i, token in enumerate(tokens):
        if is_punctuation(token):
            continue
        if is_participle(token):
            start = relative_clause_start(tokens, outers, i)
            mark_span(inners, start, i, "RELCL", "_")
            mark_span(clauses, start, i, "RELCL", "O")
            force_np_outer(outers, start, i)
        elif is_complement_verb(token):
            start = complement_clause_start(tokens, i)
            mark_span(clauses, start, i, "COMPCL", "O")

    return [
        AnnotatedToken(form=token, outer=outer, inner=inner, clause=clause)
        for token, outer, inner, clause in zip(tokens, outers, inners, clauses)
    ]


def write_conll(sentences: list[str], path: str | Path) -> None:
    output: list[str] = []
    for sentence in sentences:
        output.append(f"# text = {sentence}")
        output.append("# columns = ID FORM CHUNK-OUTER CHUNK-INNER CLAUSE")
        for index, token in enumerate(annotate_sentence(sentence), start=1):
            output.append(f"{index}\t{token.form}\t{token.outer}\t{token.inner}\t{token.clause}")
        output.append("")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create heuristic Turkish chunking annotations.")
    parser.add_argument("--input", default="dataset/raw/sentences_1000.txt")
    parser.add_argument("--output", default="dataset/processed/chunking_annotated.conll")
    parser.add_argument("--expected-count", type=int, default=1000)
    args = parser.parse_args()

    sentences = read_raw_sentences(args.input)
    if len(sentences) != args.expected_count:
        raise ValueError(f"Expected {args.expected_count} sentences, found {len(sentences)}.")
    write_conll(sentences, args.output)
    token_count = sum(len(tokenize(sentence)) for sentence in sentences)
    print(f"Wrote {len(sentences)} sentences and {token_count} tokens to {args.output}.")


if __name__ == "__main__":
    main()
