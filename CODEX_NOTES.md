# Codex İçin Proje Notları

## Çalıştırma Sırası

```bash
pip install -r requirements.txt
python src/annotate_chunking.py
python src/prepare_dataset.py
python src/train_crf.py
python src/cross_validate.py
```

## Güncel Veri ve Model Durumu

- Proje konusu: Türkçe chunking.
- Ana veri dosyası: `dataset/processed/chunking_annotated.conll`
- CoNLL kolonları: `ID FORM CHUNK-OUTER CHUNK-INNER CLAUSE`
- `prepare_dataset.py`, `CHUNK-INNER` ve `CLAUSE` kolonlarını koruyarak `train.conll` ve `test.conll` üretir.
- `train_crf.py`, `outer`, `inner` ve `clause` için ayrı CRF modelleri eğitir ve aynı pickle dosyasına kaydeder.
- Ana confusion matrix `CHUNK-OUTER` için üretilir.

## Sonuç Dosyaları

- `results/metrics.json`
- `results/cross_validation_results.json`
- `results/classification_report.txt`
- `results/classification_report_inner.txt`
- `results/classification_report_clause.txt`
- `results/confusion_matrix.png`
- `results/chunking_crf_model.pkl`

## Teslim İçin Korunacaklar

- `assignment/`
- `dataset/`
- `src/`
- `results/`
- `report/`
- `README.md`
- `requirements.txt`

Teslim zipine `.git/` ve `src/__pycache__/` gibi çalışma artıkları dahil edilmemeli.
