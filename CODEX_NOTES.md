# Codex için Yapılacaklar

1. Önce projeyi çalıştır:

```bash
pip install -r requirements.txt
python src/prepare_dataset.py
python src/train_crf.py
python src/cross_validate.py
```

2. Çıkan metrikleri `report/report_draft.md` içine işle.

3. `classification_report.txt` ve `confusion_matrix.png` sonuçlarını rapora ekle.

4. Gerekirse `features.py` dosyasına yeni feature ekle:
   - Türkçe ek bilgileri
   - noktalama kontrolü
   - kelime uzunluğu
   - önceki/sonraki iki kelime

5. Son teslim için klasörleri şu şekilde koru:
   - `dataset/`
   - `src/`
   - `results/`
   - `report/`
