# 1. Taban İmajı: Projenin çalışacağı işletim sistemi ve Python sürümü. 
# "slim" versiyonu, gereksiz her şeyi silip imajın boyutunu küçültür.
FROM python:3.11-slim

# 2. Çalışma Dizini: Konteynerin içindeki sanal bilgisayarda dosyalar nereye konulacak?
WORKDIR /app

# 3. Sistem Gereksinimleri: Linux için temel derleyicilerin kurulması.
# ChromaDB gibi vektör veritabanları arka planda derlenmeye ihtiyaç duyar.
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Kodların Kopyalanması: Bilgisayarınızdaki (veya GitHub'daki) tüm dosyaları sanal makineye (/app) kopyala.
COPY . /app

# 5. Kütüphanelerin Kurulumu: requirements.txt dosyasını okuyup her şeyi indir.
# --no-cache-dir kullanarak inen kurulum dosyalarını siliyoruz ki konteyner hafif olsun.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Port Açılması: Streamlit varsayılan olarak 8501 portunda çalışır. Dışarıya bu portu açıyoruz.
EXPOSE 8501

# 7. Sağlık Kontrolü (Healthcheck): Sunucunun uygulamanın çöküp çökmediğini anlaması için ping komutu.
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 8. Çalıştırma Komutu: Konteyner ayağa kalktığında otomatik olarak hangi komut yazılacak?
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
