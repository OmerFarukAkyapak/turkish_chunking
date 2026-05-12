# Türkçe Chunking Projesi

Bu proje, Türkçe cümlelerde sözdizimsel öbeklerin otomatik etiketlenmesi için hazırlanmıştır. Ana yöntem olarak CRF (Conditional Random Fields) kullanılır.

## Klasör Yapısı

```txt
project/
├── dataset/
│   ├── raw/
│   │   └── sentences_1000.txt
│   └── processed/
│       ├── chunking_annotated.conll
│       ├── train.conll
│       ├── test.conll
│       └── dataset_stats.txt
├── src/
│   ├── annotate_chunking.py
│   ├── data_utils.py
│   ├── features.py
│   ├── prepare_dataset.py
│   ├── train_crf.py
│   ├── cross_validate.py
│   └── predict.py
├── results/
├── report/
├── requirements.txt
└── README.md
```

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Linux/macOS için:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 1. Dataset Hazırlama

Ham 1000 cümleden chunking anotasyon dosyasını üretmek için:

```bash
python src/annotate_chunking.py
```

Bu komut şunu üretir:

```txt
dataset/processed/chunking_annotated.conll
```

Eğitim/test ayrımını üretmek için:

```bash
python src/prepare_dataset.py
```

Bu komut şunları üretir:

```txt
dataset/processed/train.conll
dataset/processed/test.conll
dataset/processed/dataset_stats.txt
```

## 2. Model Eğitimi

```bash
python src/train_crf.py
```

Bu komut şunları üretir:

```txt
results/chunking_crf_model.pkl
results/metrics.json
results/classification_report.txt
results/classification_report_inner.txt
results/classification_report_clause.txt
results/confusion_matrix.png
```

## 3. Cross-Validation

```bash
python src/cross_validate.py
```

Bu komut şunu üretir:

```txt
results/cross_validation_results.json
```

## 4. Yeni Cümle Üzerinde Tahmin

```bash
python src/predict.py --text "Keloğlan annesinden izin alıp balık tutmaya gitmiş."
```

## Kullanılan Etiketler

```txt
B-NP, I-NP
B-VP, I-VP
B-ADVP, I-ADVP
B-ADJP, I-ADJP
O
```

## Not

`dataset/raw/sentences_1000.txt` dosyası 1000 cümlelik ham/veri hazırlama dosyasıdır. Model eğitimi için `dataset/processed/chunking_annotated.conll` kullanılır. Henüz etiketlenmemiş yeni cümleler eklenirse aynı CoNLL formatında bu dosyaya dahil edilmelidir.
