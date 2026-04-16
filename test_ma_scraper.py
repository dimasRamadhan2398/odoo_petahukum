import urllib.request
import ssl
from bs4 import BeautifulSoup

def _scrape_ma():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = 'https://putusan3.mahkamahagung.go.id/direktori/index/pengadilan/mahkamah-agung/kategori/perdata-1.html'
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )

    with urllib.request.urlopen(req, context=ctx) as response:
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        links = soup.find_all('a')
        putusan_links = [l for l in links if l.get('href') and ('direktori/putusan/' in l.get('href'))]

        unique_verdicts = {}
        for l in putusan_links:
            href = l.get('href')
            text = l.text.strip()
            if href not in unique_verdicts and "Nomor" in text:
                unique_verdicts[href] = text

        print(f"Found {len(unique_verdicts)} potential verdicts")
        for href, text in list(unique_verdicts.items())[:5]:
            name = text.replace('Putusan MAHKAMAH AGUNG Nomor', '').strip()
            print(f"Name: {name}, Judul: {text}, URL: {href}")

_scrape_ma()
