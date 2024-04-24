import requests
from bs4 import BeautifulSoup


class PageFocus():
    def __init__(self):
        super().__init__()

    def request_page(self, url):
        response : str = requests.get(url).text
        return self.soup(response)

    def soup(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        return soup