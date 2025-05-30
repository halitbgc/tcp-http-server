# 1) Base image
FROM python:3.11-slim

# 2) Uygulama klasörünü oluştur ve ayarla
WORKDIR /app

# 3) Kodları kopyala
COPY server.py ./
COPY static ./static

# 4) Portu expose et
EXPOSE 8080

# 5) Çalıştırma komutu
CMD ["python", "server.py"]
