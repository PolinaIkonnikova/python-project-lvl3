from urllib.parse import urlparse
import os, tempfile
import requests
import requests_mock

url = 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/ReiManga.jpg/170px-ReiManga.jpg'
a = os.path.abspath(os.path.join('.', '1.py'))
b = os.path.abspath(os.path.join('.'))
#print(os.path.isdir(a), os.path.isdir(b))
url1 = urlparse('/wikipedia/en/thumb/e/e1/ReiManga.jpg/170px-ReiManga.jpg')
old_url = urlparse('https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/ReiManga.jpg/170px-ReiManga.jpg')
old_url.scheme
old_url.netloc
#print(url1)
new_url = url1._replace(scheme=old_url.scheme, netloc = old_url.netloc)
#print(urlunparse(new_url))
path_body, ending = os.path.splitext("https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/ReiManga.jpg/170px-ReiManga.jpg")
#print(ending)
with tempfile.TemporaryDirectory() as temp:
    print()

