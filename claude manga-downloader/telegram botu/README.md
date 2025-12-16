# 🤖 Manga Downloader Telegram Bot

Telegram üzerinden manga indirme botu!

## 🎯 Nasıl Çalışır?

1. **Telegram'da Bot'a Yazarsınız:**
   ```
   https://asuracomic.net/series/manga-name
   ```

2. **Bot Chapter Listesi Gönderir:**
   ```
   ✅ Bulundu!
   📚 Manga: The Greatest Estate Developer  
   📖 Chapter Sayısı: 218
   
   Hangi chapter'ları istersiniz?
   ```

3. **Siz Seçersiniz:**
   ```
   1-10
   ```
   veya
   ```
   50
   ```
   veya
   ```
   all
   ```

4. **Bot PDF Gönderir!** 📥

---

## 📲 Kurulum (Adım Adım)

### 1️⃣ Telegram Bot Oluştur

1. Telegram'da [@BotFather](https://t.me/BotFather) ara
2. `/newbot` komutunu gönder
3. Bot için isim seç (örn: "Manga Downloader")
4. Bot için username seç (örn: "my_manga_bot")
5. **Bot Token'ı kopyala** (örn: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2️⃣ Python Kurulumu

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 3️⃣ Bot Token'ı Ayarla

`telegram_bot.py` dosyasını aç ve şu satırı bul:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

BotFather'dan aldığın token'ı buraya yapıştır:

```python
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
```

### 4️⃣ Bot'u Başlat

```bash
python telegram_bot.py
```

Şunu göreceksin:
```
🤖 Bot starting...
```

### 5️⃣ Kullanmaya Başla!

1. Telegram'da kendi botunu ara (username'i kullan)
2. `/start` komutunu gönder
3. Manga linki gönder
4. Chapter seç
5. PDF'i indir! 🎉

---

## 💡 Kullanım Örnekleri

### Örnek 1: İlk 10 Chapter
```
Siz: https://asuracomic.net/series/manga-name
Bot: ✅ Bulundu! 218 chapter var.
Siz: 1-10
Bot: [PDF dosyası gönderir]
```

### Örnek 2: Belirli Bir Chapter
```
Siz: https://asuracomic.net/series/manga-name
Bot: ✅ Bulundu! 218 chapter var.
Siz: 50
Bot: [50. chapter PDF olarak]
```

### Örnek 3: Tüm Chapter'lar
```
Siz: https://asuracomic.net/series/manga-name
Bot: ✅ Bulundu! 218 chapter var.
Siz: all
Bot: [Tüm chapter'ları PDF olarak - DİKKAT: uzun sürebilir!]
```

### Örnek 4: Karışık Seçim
```
Siz: 1-5,10,15-20
Bot: [1,2,3,4,5,10,15,16,17,18,19,20. chapter'ları gönderir]
```

---

## 🎮 Komutlar

- `/start` - Botu başlat
- `/help` - Yardım
- `/cancel` - İşlemi iptal et

---

## ⚙️ Özellikler

✅ **Kolay Kullanım:** Sadece link gönder
✅ **Mobil Uyumlu:** Telegram'dan her yerden kullan
✅ **Hızlı:** Chapter listesi saniyeler içinde
✅ **PDF Oluşturma:** Direkt PDF dosyası
✅ **Desteklenen Siteler:**
   - Asura Scans
   - MangaDex
   - Manganato
   - Diğerleri (deneysel)

---

## ⚠️ Önemli Notlar

1. **İlk Kullanım:** 1-5 chapter ile test edin
2. **Dosya Boyutu:** Telegram limiti 50MB
3. **Süre:** Çok chapter seçerseniz dakikalar sürebilir
4. **İnternet:** Bot'un çalıştığı yerde internet olmalı
5. **Chrome:** Selenium için Chrome/Chromium gerekli

---

## 🐛 Sorun Giderme

### "Bot yanıt vermiyor"
- Bot'un çalıştığından emin olun (`python telegram_bot.py`)
- Token'ı doğru kopyaladınız mı?

### "Chapter bulunamadı"
- Link doğru mu kontrol edin
- Site değişmiş olabilir

### "PDF oluşturulamadı"
- Daha az chapter seçin
- İnternet bağlantınızı kontrol edin

### "Chrome driver hatası"
- Chrome/Chromium yükleyin:
  ```bash
  # Linux
  sudo apt install chromium-browser
  
  # Windows: Chrome zaten yüklü ise sorun yok
  ```

---

## 🚀 Gelişmiş: Sunucuda Çalıştırma

Bot'u 7/24 çalışır hale getirmek için:

### Option 1: PythonAnywhere (Ücretsiz)
1. [pythonanywhere.com](https://pythonanywhere.com) hesap aç
2. Bot dosyalarını yükle
3. "Always on task" olarak ayarla

### Option 2: Railway / Render
1. GitHub'a yükle
2. Railway/Render'a bağla
3. Otomatik deploy

### Option 3: VPS (DigitalOcean, etc.)
```bash
# Screen kullanarak arka planda çalıştır
screen -S manga-bot
python telegram_bot.py
# Ctrl+A+D ile detach
```

---

## 📝 Notlar

- Bu bot **kişisel kullanım** içindir
- Telif haklarına dikkat edin
- Rate limiting uygulanmıştır
- Sunuculara fazla yük bindirmeyin

---

## 🎨 Özelleştirme

Bot kodunda şunları değiştirebilirsiniz:

- Maksimum chapter sayısı (şu an 20)
- PDF formatı ve stil
- Desteklenen siteler
- Mesaj metinleri

---

**Made with 💜 by Claude**

Sorularınız için: Telegram'da bana yazın! 😊
