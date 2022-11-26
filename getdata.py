from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://bulbapedia.bulbagarden.net/wiki/List_of_moves_that_do_damage"

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
# Retrieve Data from Website
html = urlopen(req).read()
soup = BeautifulSoup(html, "html.parser")
soup = soup.prettify()
soupstring = str(soup)

filename = "movedatahtml.txt"
file = open(filename, 'w')
file.write(soupstring)
file.close()
