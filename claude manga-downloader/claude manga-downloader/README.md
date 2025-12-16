# 📚 Manga Downloader - Backend + Frontend

Manga sitelerinden chapter listelerini çıkarıp PDF olarak indiren tam işlevsel uygulama.

## 🚀 Özellikler

- ✅ **Desteklenen Siteler:**
  - MangaDex (API ile)
  - Manganato / Chapmanganato
  - Mangakakalot
  - Asura Scans
  - Diğer siteler (otomatik algılama)

- ✅ **İşlevler:**
  - Link ile chapter listesi tarama
  - Çoklu chapter seçimi
  - PDF oluşturma ve indirme
  - Progress tracking
  - Retro-futuristik anime UI

## 📦 Kurulum

### 1. Python Bağımlılıklarını Yükle

```bash
cd manga-backend
pip install -r requirements.txt
```

### 2. Backend'i Başlat

```bash
python app.py
```

Backend `http://localhost:5000` adresinde çalışacak.

### 3. Frontend'i Aç

`index.html` dosyasını tarayıcınızda açın. Çift tıklayarak açabilirsiniz.

## 🎮 Kullanım

1. Backend'in çalıştığından emin olun (yeşil ✓ görmelisiniz)
2. Manga linkini yapıştırın
3. "TARA" butonuna basın
4. Chapter'ları seçin
5. "PDF OLARAK İNDİR" butonuna basın
6. PDF dosyanız indirilecek!

## 🔧 API Endpoints

### POST /api/scrape
Manga URL'sinden chapter listesi çıkarır.

**Request:**
```json
{
  "url": "https://mangawebsite.com/manga/..."
}
```

**Response:**
```json
{
  "title": "Manga Name",
  "chapters": [
    {
      "number": "1",
      "title": "Chapter 1 Title",
      "url": "chapter_url"
    }
  ]
}
```

### POST /api/download
Seçili chapterları PDF olarak indirir.

**Request:**
```json
{
  "title": "Manga Name",
  "chapters": [
    {
      "number": "1",
      "title": "Chapter 1",
      "url": "chapter_url"
    }
  ]
}
```

**Response:** PDF file download

## 🐛 Sorun Giderme

### Backend bağlanamıyor
- Backend'in çalıştığından emin olun: `python app.py`
- Port 5000'in kullanılabilir olduğundan emin olun
- Firewall ayarlarını kontrol edin

### Chapter bulunamıyor
- Link'in doğru olduğundan emin olun
- Site yapısı değişmiş olabilir
- Farklı bir site deneyin

### PDF oluşturulmuyor
- İnternet bağlantınızı kontrol edin
- Bazı siteler anti-bot koruması kullanabilir
- Daha az chapter seçerek deneyin

## 🔮 Sonraki Adımlar

### Android APK için:
1. React Native veya Capacitor kullanarak port et
2. Offline storage ekle
3. Background download desteği ekle

### Geliştirmeler:
- [ ] Daha fazla site desteği
- [ ] Gelişmiş PDF formatlaması
- [ ] Batch download
- [ ] Download queue
- [ ] Offline okuma
- [ ] Cloud sync

## ⚠️ Önemli Notlar

- Bu araç sadece **kişisel kullanım** içindir
- Telif hakkı yasalarına uyun
- Sunuculara yük bindirmemek için dikkatli kullanın
- Rate limiting uygulanmıştır (chapter başına 0.5 saniye)

## 📝 Lisans

Eğitim amaçlıdır. Kendi sorumluluğunuzda kullanın.

---

**Made with 💜 by Claude**
