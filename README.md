# Petglare Workshop

[Petglare](https://github.com/Baglare/ClaudePetGlare) masaüstü maskotu için topluluk pet kataloğu. Petglare'da **Ayarlar → Workshop'a bağlan** açıkken **Workshop'tan pet bul…** bu kataloğu gösterir; seçtiğin pet bilgisayarına indirilir ve doğrulanır.

## Pet gönderme

1. Petglare'da **Ayarlar → Şekil** satırında kendi pet'ine sağ tıkla → **Workshop'a gönder…**
2. Açılan GitHub formuna Petglare'ın hazırladığı PNG'yi sürükle, adı yaz, onayları işaretle ve gönder.
3. Bir bot görseli denetler (PNG, en çok 2 MB ve 4096 piksel), yeniden kodlar, 512 piksele küçültür ve onay için bir PR açar.
4. Bakımcı onaylayıp birleştirince pet kataloğa girer.

Formu elle de açabilirsin: [Pet gönder](../../issues/new?template=pet.yml).

## Kurallar

- Yalnız kendi yaptığın veya paylaşma hakkın olan görseller.
- Uygunsuz, şiddet veya nefret içeren içerik kabul edilmez.
- Gönderilen görseller [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.tr) ile paylaşılır; yazar adı katalogda görünür.
- Kaldırılmasını istediğin bir pet için issue aç.

## Yapı

| Yol | İçerik |
|---|---|
| `pets/<id>/pet.png` | Şeffaf arka planlı pet, en çok 512 px ve 300 KB |
| `pets/<id>/pet.json` | Ad, yazar, tarih, SHA-256, gönderim issue'su |
| `index.json` | Birleştirmeden sonra otomatik üretilen katalog |
| `scripts/` | Gönderim denetimi ve katalog üretimi (Python + Pillow) |
