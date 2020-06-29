import bs4
import requests


def get_data_from_url(url: str):
    if url is None:
        return 500, None, None
    response = requests.get(url)
    status_code = response.status_code if response is not None else 500
    if response is not None and response.status_code < 400:
        html = bs4.BeautifulSoup(response.text, 'html.parser')
        page_title = html.find("title").text
        paragraphs = [p.text.strip() for p in html.find_all("p")
                      if p.text != "\n"]
        text = ' '.join(paragraphs)
        text = text.replace("\n", " ")
        return status_code, page_title, text
    return status_code, None, None
