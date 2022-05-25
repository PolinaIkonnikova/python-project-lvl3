from urllib.parse import urlparse
import os, tempfile


url = 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/ReiManga.jpg/170px-ReiManga.jpg'
url1 = urlparse('/wikipedia/en/thumb/e/e1/ReiManga.jpg/170px-ReiManga.jpg')
old_url = urlparse('https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/ReiManga.jpg/170px-ReiManga.jpg')
old_url.scheme
old_url.netloc
#print(url1)
new_url = url1._replace(scheme=old_url.scheme, netloc = old_url.netloc)
#print(urlunparse(new_url))
path_body, ending = os.path.splitext("https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/ReiManga.jpg/170px-ReiManga.jpg")
#print(ending)
with requests_mock.Mocker() as m:
    m.get('https://ru.hexlet.io/courses', text=open('html_before.html', 'r').read())
    print(requests.get('https://ru.hexlet.io/courses').text)
