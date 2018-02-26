import requests
from bs4 import BeautifulSoup

url = 'https://www.letras.mus.br/joao-gilberto/100377/'
source_code = requests.get(url)
text = source_code.text
soup = BeautifulSoup(text, "lxml")

data = soup.select("#breadcrumb a span")
print(data[1].find_all(text=True))