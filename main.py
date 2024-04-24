from src.helper.hard_code import HardCode
import logging
from logging import handlers

class Main(HardCode):
    def __init__(self):
        super().__init__()

    def _main(self, link_main):
        self.url = link_main
        soup = self.request_page(self.url)
        links = [f"https://www.worlddata.info{a.get('href')}" for a in soup.find(id='topnav').find_all('a') if a.get('data-navbar')]
        total = []
        for link in links:
            self.url = link
            soup = self.request_page(self.url)
            links = [f"https://www.worlddata.info{a.get('href')}" for a in soup.find(class_='countrylist').find_all('a')]
            total.append(len(links))
            for link in links:
                self.url = link

                try:
                    logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ] :: %(message)s',
                                        datefmt="%Y-%m-%dT%H:%M:%S", handlers=[
                            handlers.RotatingFileHandler(f'success.log'),
                            logging.StreamHandler()
                        ])
                    soup = self.request_page(self.url)
                    self.container(soup)
                    logging.info(f"success processing {self.url}")

                except Exception as e:
                    logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ] :: %(message)s',
                                        datefmt="%Y-%m-%dT%H:%M:%S", handlers=[
                            handlers.RotatingFileHandler(f'error.log'),
                            logging.StreamHandler()
                        ])
                    logging.error(f"Error occurred while processing {self.url}: {str(e)}")
        print(
            total
        )


if __name__ == "__main__":
    Main()._main(
        link_main='https://www.worlddata.info'
    )
