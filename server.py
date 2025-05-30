import json
import os
import socket
import threading
import mimetypes
from datetime import datetime

# Sunucu adresi ve port numarası
HOST, PORT = '0.0.0.0', 8080

# Statik dosyaların bulunduğu dizin
STATIC_DIR = 'static'

def route_request(method, path, headers, body_bytes):
    """
    API uç noktalarına gelen istekleri yönlendirir.
    - GET /api/hello: "Hello, world!" mesajı döner.
    - POST /api/echo: Gönderilen JSON veriyi aynen geri döner.
    Diğer durumlarda 404 döndürür.
    """
    # "Hello" endpoint'i
    if method == 'GET' and path == '/api/hello':
        payload = {"message": "Hello, world!"}
        data = json.dumps(payload).encode('utf-8')
        return 200, 'application/json', data

    # Echo endpoint'i: gelen JSON verisini geri çevir
    if method == 'POST' and path == '/api/echo':
        try:
            recv = json.loads(body_bytes.decode('utf-8'))
        except json.JSONDecodeError:
            recv = {"error": "Invalid JSON"}
        data = json.dumps(recv).encode('utf-8')
        return 200, 'application/json', data

    # Bulunamayan API yolu → 404
    return 404, 'application/json', b'{"error":"Not found"}'


def handle_client(conn, addr):
    """
    Bağlanan istemciyi ele alır:
    - HTTP isteğini okur ve parçalar.
    - API çağrılarını route_request ile işler.
    - Statik dosyalar için dosya sisteminden içerik döner.
    - Hataları yakalar ve 500 Internal Server Error mesajı oluşturur.
    """
    try:
        # İstek verisini oku (en fazla 4096 bayt)
        request = conn.recv(4096).decode('utf-8', errors='ignore')
        lines = request.splitlines()
        if not lines:
            # Boş istek → hemen çık
            return

        # İlk satırdan yöntemi (GET/POST) ve yolu al
        method, path, _ = lines[0].split()

        # Başlıkları (headers) ayrıştır
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            k, v = lines[i].split(':', 1)
            headers[k.strip().lower()] = v.strip()
            i += 1

        # POST isteği ise body içeriğini oku
        body_bytes = b''
        if method == 'POST':
            length = int(headers.get('content-length', 0))
            sep = '\r\n\r\n'
            idx = request.find(sep)
            if idx != -1:
                # Header ile body arasındaki ayırıcıyı bul ve body kısmını al
                body_bytes = request[idx+len(sep):].encode('utf-8', errors='ignore')
                while len(body_bytes) < length:
                    body_bytes += conn.recv(4096)

        # API rotalarını işleme
        if path.startswith('/api/'):
            status, content_type, resp_body = route_request(method, path, headers, body_bytes)
            header = (
                f'HTTP/1.1 {status} {"OK" if status==200 else "Error"}\r\n'
                f'Content-Type: {content_type}\r\n'
                f'Content-Length: {len(resp_body)}\r\n'
                '\r\n'
            ).encode('utf-8')
            conn.sendall(header + resp_body)
            print_log(addr, method, path, status)
            return

        # Statik dosya servisi
        if path == '/':
            # Ana sayfa isteği => index.html göster
            path = '/index.html'
        file_path = os.path.join(STATIC_DIR, path.lstrip('/'))
        if os.path.isfile(file_path):
            # Dosya varsa içeriği oku ve MIME tipini belirle
            ctype, _ = mimetypes.guess_type(file_path)
            if ctype is None:
                ctype = 'application/octet-stream'
            with open(file_path, 'rb') as f:
                content = f.read()
            header = (
                'HTTP/1.1 200 OK\r\n'
                f'Content-Type: {ctype}\r\n'
                f'Content-Length: {len(content)}\r\n'
                '\r\n'
            ).encode('utf-8')
            conn.sendall(header + content)
            status = 200
        else:
            # Dosya bulunamazsa 404 döndür
            body = b'<h1>404 Not Found</h1>'
            header = (
                'HTTP/1.1 404 Not Found\r\n'
                'Content-Type: text/html\r\n'
                f'Content-Length: {len(body)}\r\n'
                '\r\n'
            ).encode('utf-8')
            conn.sendall(header + body)
            status = 404

        print_log(addr, method, path, status)

    except Exception as e:
        # Beklenmedik hata durumu → 500 Internal Server Error
        error_body = f'<h1>500 Internal Server Error</h1><pre>{e}</pre>'.encode('utf-8')
        header = (
            'HTTP/1.1 500 Internal Server Error\r\n'
            'Content-Type: text/html\r\n'
            f'Content-Length: {len(error_body)}\r\n'
            '\r\n'
        ).encode('utf-8')
        conn.sendall(header + error_body)
        print_log(addr, method if 'method' in locals() else '-', path if 'path' in locals() else '-', 500)
    finally:
        conn.close()


def print_log(addr, method, path, status):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{now}] {addr[0]} {method} {path} → {status}')

# Ana fonksiyon
def main():
    """
    Sunucuyu başlatır ve gelen bağlantılar için yeni thread açar.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Adresin tekrar kullanılmasına izin ver
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f'Listening on {HOST}:{PORT}…')
        while True:
            # Yeni bağlantı kabul et ve işlemek üzere yeni bir thread başlat
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# main fonksiyonu calistirma
if __name__ == '__main__':
    main()
