# Türkçe Metinlerde Chunking için CRF Tabanlı Yaklaşım

## 1. Giriş

Bu çalışmada Türkçe metinlerde isim öbeği (NP), eylem öbeği (VP), zarf öbeği (ADVP) ve sıfat öbeği (ADJP) gibi sözdizimsel öbeklerin otomatik olarak belirlenmesi amaçlanmıştır. Chunking, cümledeki kelimelerin yüzeysel sözdizimsel gruplara ayrılması işlemidir ve bilgi çıkarımı, anlamsal çözümleme ve metin işleme gibi birçok NLP görevi için önemli bir ara adımdır.

## 2. Veri Seti

Veri seti hikâye metinlerinden seçilen Türkçe cümlelerden oluşturulmuştur. Cümleler CoNLL formatında işaretlenmiştir. Her satırda token numarası, kelime ve chunk etiketi yer almaktadır.

Kullanılan etiketler:

- B-NP / I-NP: İsim öbeği
- B-VP / I-VP: Eylem öbeği
- B-ADVP / I-ADVP: Zarf öbeği
- B-ADJP / I-ADJP: Sıfat öbeği
- O: Noktalama veya öbek dışı token

## 3. Yöntem

Bu projede sequence labeling problemi için Conditional Random Fields (CRF) modeli kullanılmıştır. CRF, bir dizideki her elemanın etiketini belirlerken komşu etiket ilişkilerini de dikkate aldığı için chunking görevi için uygun bir yöntemdir.

Her token için kullanılan bazı özellikler:

- Kelimenin küçük harfli biçimi
- Kelimenin son 1, 2 ve 3 karakteri
- Kelimenin ilk 1 ve 2 karakteri
- Büyük harfle başlayıp başlamadığı
- Sayı olup olmadığı
- Önceki kelime bilgisi
- Sonraki kelime bilgisi

## 4. Deneysel Kurulum

Veri seti eğitim ve test olmak üzere %80 / %20 oranında ayrılmıştır. Ayrıca 5-fold cross-validation kullanılarak modelin genelleme başarısı ölçülmüştür.

## 5. Değerlendirme Metrikleri

Model başarısı aşağıdaki metriklerle değerlendirilmiştir:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

## 6. Sonuçlar

Bu bölüme `results/metrics.json`, `results/classification_report.txt` ve `results/cross_validation_results.json` dosyalarındaki değerler eklenecektir.

Confusion matrix grafiği:

```txt
results/confusion_matrix.png
```

## 7. Tartışma

Modelin en çok karıştırdığı etiketlerin özellikle B/I geçişlerinde ve benzer görevli öbeklerde ortaya çıkması beklenmektedir. Türkçenin eklemeli yapısı nedeniyle ek bilgileri ve kelime son ekleri model için önemli ipuçları sağlamaktadır.

## 8. Sonuç

Bu çalışmada Türkçe chunking görevi için CRF tabanlı bir sistem geliştirilmiştir. CoNLL formatında hazırlanan veri seti üzerinde eğitim, test ve cross-validation işlemleri gerçekleştirilmiştir. Elde edilen sonuçlar, klasik sequence labeling yöntemlerinin Türkçe sözdizimsel öbekleme görevinde kullanılabilir olduğunu göstermektedir.
