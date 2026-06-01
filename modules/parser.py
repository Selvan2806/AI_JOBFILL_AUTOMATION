from bs4 import BeautifulSoup


class JobParser:

    def extract_text(self, html):

        soup = BeautifulSoup(html, "lxml")

        return soup.get_text(separator=" ", strip=True)