# MaydaGold Altın Fiyatları API

Bu proje, anlık altın fiyatlarını çekmek ve JSON formatında sunmak amacıyla geliştirilmiş, Python (Flask) tabanlı bir REST API servisidir. `maydagold.com` üzerindeki verileri anlık olarak işler ve temizlenmiş veri olarak döndürür.

## 🚀 Özellikler

- **Anlık Veri:** Kaynak siteden canlı veri çekimi.
- **Temiz Veri:** Fiyatlardaki binlik ayracı ve para birimi sembollerini temizleyerek `float` (sayısal) formatta sunar.
- **JSON Çıktısı:** Mobil uygulamalar ve web siteleri için kolay entegrasyon.
- **Türkiye Saati:** Sunucu saati fark etmeksizin `Europe/Istanbul` zaman dilimini kullanır.

## 🛠 Kurulum ve Çalıştırma

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Depoyu klonlayın:**
   
   git clone [https://github.com/gkhnnnll/maydapi.git](https://github.com/gkhnnnll/maydapi.git)
   cd maydapi

2.Gerekli kütüphaneleri yükleyin:

 pip install -r requirements.txt

3. Uygulamayı başlatın:
   
python main.py


Tarayıcınızda http://127.0.0.1:5000/api/gold adresine giderek test edebilirsiniz.

📡 API Kullanımı
Endpoint: /api/gold
İstek Türü: GET

Örnek Yanıt:

JSON

{
  "kaynak": "maydagold.com",
  "güncelleme_zamanı": "2025-11-18 17:30:00",
  "fiyatlar": {
    "HASHas Altın": {
      "alış": 5731.0,
      "satış": 5800.5,
      "alış_str": "5.731,00",
      "satış_str": "5.800,50"
    },
    "ÇEYREKÇeyrek Altın": {
      "alış": 9285.0,
      "satış": 9415.0,
      "alış_str": "9.285",
      "satış_str": "9.415"
    }
  }
}



⚠️ Yasal Uyarı
Bu proje sadece eğitim ve kişisel kullanım amaçlıdır. Veriler üçüncü taraf bir web sitesinden çekilmektedir. Yatırım tavsiyesi içermez ve verilerin kesin doğruluğu garanti edilmez.
