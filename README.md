# kelime-sozluk

Sesli Kelime Oyunu için İngilizce ⇄ Türkçe sözlük dosyaları. Sunucu gerektirmez;
dosyalar jsDelivr CDN üzerinden ücretsiz ve kotasız sunulur.

```
https://cdn.jsdelivr.net/gh/<KULLANICI>/kelime-sozluk@main/data/A1.json
```

## Dosya yapısı
`data/A1.json … data/C1.json` (C1 dosyası C1 ve C2 kelimelerini içerir)

```json
{
  "w": { "house": [["ev",100],["hane",87]] },        // İngilizce -> Türkçe karşılıklar ve puanları
  "r": { "ev":    [["home",90],["residence",54]] }   // Türkçe soru kelimesi -> ek İngilizce karşılıklar
}
```
Puanlar 0–100 arasındadır; en olası karşılık 100 alır.

## Kaynaklar ve lisans
- Çeviriler: [Wiktionary](https://en.wiktionary.org) — İngilizce→Türkçe çeviri tabloları
  ([open-dsl-dict/wiktionary-dict](https://github.com/open-dsl-dict/wiktionary-dict)) ve Türkçe maddeler
  ([Vuizur/Wiktionary-Dictionaries](https://github.com/Vuizur/Wiktionary-Dictionaries), kaikki.org/wiktextract).
  Lisans: **CC BY-SA 3.0** ve GFDL. Bu klasördeki veriler de aynı lisansla (CC BY-SA 3.0) paylaşılmıştır.
- Seviyeler: [CEFR-J Vocabulary Profile](https://github.com/openlanguageprofiles/olp-en-cefrj) ve
  Octanove C1/C2 Vocabulary Profile (CC BY-SA 4.0).
- Puanlamada kelime sıklığı: [wordfreq](https://github.com/rspeer/wordfreq) (veri: CC BY-SA 4.0).

`tools/build.py` dosyaları üreten betiktir (kaynak veriler ayrıca indirilmelidir).
