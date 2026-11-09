
from pathlib import Path
from urllib.parse import quote
from xml.etree import ElementTree as ET

# Địa chỉ website
SITE_URL = "https://motgocphatphap.com".rstrip("/")

# Thư mục gốc của website
ROOT = Path(__file__).resolve().parent

# Kiểm tra cấu trúc website
index_file = ROOT / "index.html"
books_dir = ROOT / "books"

if not index_file.is_file():
    raise FileNotFoundError("Không tìm thấy index.html!")

if not books_dir.is_dir():
    raise FileNotFoundError("Không tìm thấy thư mục books!")

# Lấy trang chủ và các ebook HTML
pages = [index_file]
pages.extend(
    page for page in sorted(books_dir.glob("*.html"))
    if page.name != "template.html"
)

# Tạo sitemap XML
namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", namespace)

urlset = ET.Element(f"{{{namespace}}}urlset")

for page in pages:
    relative_path = page.relative_to(ROOT).as_posix()

    if relative_path == "index.html":
        url = SITE_URL + "/"
    else:
        # Mã hóa ký tự đặc biệt trong đường dẫn URL
        encoded_path = quote(relative_path, safe="/-._~")
        url = f"{SITE_URL}/{encoded_path}"

    url_element = ET.SubElement(urlset, f"{{{namespace}}}url")
    loc = ET.SubElement(url_element, f"{{{namespace}}}loc")
    loc.text = url

# Ghi sitemap.xml
tree = ET.ElementTree(urlset)
tree.write(
    ROOT / "sitemap.xml",
    encoding="UTF-8",
    xml_declaration=True
)

print(f"Đã tạo sitemap.xml với {len(pages)} trang.")
