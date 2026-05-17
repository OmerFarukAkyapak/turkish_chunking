# Türkçe Chunking Projesi

Bu proje, Türkçe cümlelerde sözdizimsel öbeklerin otomatik etiketlenmesi için hazırlanmıştır. Ana yöntem olarak CRF (Conditional Random Fields) kullanılır.

Proje, CoNLL formatında `CHUNK-OUTER`, `CHUNK-INNER` ve `CLAUSE` kolonlarını üretir ve bu üç kolon için ayrı CRF modeli eğitir.

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
│   ├── plot_results.py
│   └── predict.py
├── results/
├── report/
├── requirements.txt
└── README.md
```

## Kurulum

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Çalıştırma Sırası

Tüm veri hazırlama, eğitim, değerlendirme ve grafik üretimi için aşağıdaki komutlar sırayla çalıştırılır:

```bash
python src/annotate_chunking.py
python src/prepare_dataset.py
python src/train_crf.py
python src/cross_validate.py
python src/plot_results.py
```

## 1. Dataset Hazırlama

Ham 1000 cümleden CoNLL formatında chunking anotasyon dosyası üretmek için:

```bash
python src/annotate_chunking.py
```

Üretilen dosya:

```txt
dataset/processed/chunking_annotated.conll
```

CoNLL kolonları:

```txt
ID FORM CHUNK-OUTER CHUNK-INNER CLAUSE
```

Eğitim/test ayrımını üretmek için:

```bash
python src/prepare_dataset.py
```

Üretilen dosyalar:

```txt
dataset/processed/train.conll
dataset/processed/test.conll
dataset/processed/dataset_stats.txt
```

Güncel veri özeti:

```txt
Sentence count: 1000
Token count: 11458
Train sentence count: 800
Test sentence count: 200
```

## 2. Model Eğitimi

```bash
python src/train_crf.py
```

Bu komut `CHUNK-OUTER`, `CHUNK-INNER` ve `CLAUSE` için ayrı CRF modelleri eğitir.

Üretilen dosyalar:

```txt
results/chunking_crf_model.pkl
results/metrics.json
results/per_class_metrics.json
results/classification_report.txt
results/classification_report_inner.txt
results/classification_report_clause.txt
results/confusion_matrix.png
results/confusion_matrix_inner.png
results/confusion_matrix_clause.png
```

## 3. Cross-Validation

```bash
python src/cross_validate.py
```

Üretilen dosya:

```txt
results/cross_validation_results.json
```

## 4. Grafik Üretimi

```bash
python src/plot_results.py
```

Üretilen grafikler:

```txt
results/per_class_metrics.png
results/cross_validation_scores.png
results/column_metrics_comparison.png
```

Grafiklerin içerikleri:

- `per_class_metrics.png`: Ana chunk etiketleri için precision, recall, F1-score ve sınıf bazlı accuracy.
- `cross_validation_scores.png`: 5-fold cross-validation boyunca accuracy ve weighted F1 değişimi.
- `column_metrics_comparison.png`: `CHUNK-OUTER`, `CHUNK-INNER` ve `CLAUSE` kolonlarının genel metrik karşılaştırması.
- `confusion_matrix.png`: Ana chunk etiketleri için karışıklık matrisi.
- `confusion_matrix_inner.png`: İç içe öbek etiketleri için karışıklık matrisi.
- `confusion_matrix_clause.png`: Yan cümle etiketleri için karışıklık matrisi.

## 5. Yeni Cümle Üzerinde Tahmin

```bash
python src/predict.py --text "Keloğlan annesinden izin alıp balık tutmaya gitmiş."
```

Örnek çıktı formatı:

```txt
# columns = ID FORM CHUNK-OUTER CHUNK-INNER CLAUSE
1	Keloğlan	B-NP	_	O
...
```

## Kullanılan Etiketler

Ana chunk etiketleri:

```txt
B-NP, I-NP
B-VP, I-VP
B-ADVP, I-ADVP
B-ADJP
O
```

İç içe öbek ve yan cümle etiketleri:

```txt
B-RELCL, I-RELCL
B-COMPCL, I-COMPCL
_
O
```

## Güncel Sonuç Özeti

Test kümesi üzerinde:

```txt
CHUNK-OUTER  accuracy=0.9334  weighted_f1=0.9330
CHUNK-INNER  accuracy=0.9650  weighted_f1=0.9571
CLAUSE       accuracy=0.9219  weighted_f1=0.9063
```

5-fold cross-validation ortalaması:

```txt
accuracy=0.9341
weighted_precision=0.9348
weighted_recall=0.9341
weighted_f1=0.9336
```

## Not

`dataset/raw/sentences_1000.txt` dosyası 1000 cümlelik ham veri dosyasıdır. Model eğitimi için `dataset/processed/chunking_annotated.conll` kullanılır. Henüz etiketlenmemiş yeni cümleler eklenirse aynı CoNLL formatında bu dosyaya dahil edilmelidir.
