from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

app = Flask(__name__)

def clean_currency(text):
    """
    Gelen string fiyatı (örn: '5,721.00' veya '5.721,00') düzgün float'a çevirir.
    """
    if not text:
        return None
    
    # Temizlik yap (TL, boşluk vs kaldır)
    clean_text = text.replace('TL', '').strip()
    
    # Eğer virgül sonda ise (kuruş ayracı) ve nokta binlik ise (TR Formatı: 1.234,56)
    if ',' in clean_text and '.' in clean_text:
        if clean_text.find('.') < clean_text.find(','):
            clean_text = clean_text.replace('.', '').replace(',', '.')
        else:
            # US Formatı (1,234.56) -> Virgülü kaldır
            clean_text = clean_text.replace(',', '')
    elif ',' in clean_text:
        # Sadece virgül varsa ve 3 haneden sonra geliyorsa binliktir (5,721) -> kaldır
        # Ama 12,50 gibiyse kuruştur. Bu ayrımı basitçe şöyle yapalım:
        if len(clean_text.split(',')[1]) == 3: # Binlik olma ihtimali yüksek
             clean_text = clean_text.replace(',', '')
        else:
             clean_text = clean_text.replace(',', '.')
            
    try:
        return float(clean_text)
    except ValueError:
        return None

def maydagold_scraper():
    url = "https://maydagold.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"hata": f"Siteye bağlanılamadı: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")
    tablo = soup.find("tbody")

    if not tablo:
        return {"hata": "Fiyat tablosu bulunamadı, site yapısı değişmiş olabilir."}

    sonuc = {
        "kaynak": "maydagold.com",
        "güncelleme_zamanı": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fiyatlar": {}
    }

    for satir in tablo.find_all("tr"):
        hücreler = satir.find_all("td")
        if len(hücreler) < 3:
            continue

        isim = hücreler[0].get_text(strip=True)
        if not isim:
            continue

        alis_str = hücreler[1].get_text(strip=True)
        satis_str = hücreler[2].get_text(strip=True)

        # Yeni temizleme fonksiyonunu kullanıyoruz
        alis = clean_currency(alis_str)
        satis = clean_currency(satis_str)

        sonuc["fiyatlar"][isim] = {
            "alış": alis,
            "satış": satis,
            "alış_str": alis_str,
            "satış_str": satis_str
        }

    return sonuc

@app.route('/')
def home():
    return jsonify({
        "mesaj": "MaydaGold API Calisiyor kankam", 
        "kullanim": "/api/gold adresine git"
    })

@app.route('/api/gold', methods=['GET'])
def get_gold_prices():
    data = maydagold_scraper()
    # JSON çıktısını UTF-8 karakter sorunu olmadan verelim
    return app.response_class(
        response=json.dumps(data, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )

if __name__ == "__main__":
    # Yerelde çalıştırırken debug açık olsun
    app.run(debug=True)