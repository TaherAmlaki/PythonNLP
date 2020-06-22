import bs4
import requests


def get_data_from_title(wiki_page_title: str):
    url = f"https://en.wikipedia.org/wiki/{wiki_page_title.title()}"
    return get_data_from_full_url(url)


def get_data_from_full_url(url: str):
    response = requests.get(url)
    status_code = response.status_code if response is not None else 500
    if response is not None and response.status_code < 400:
        html = bs4.BeautifulSoup(response.text, 'html.parser')
        page_title = html.find(id="firstHeading").text
        paragraphs = [p.text.strip() for p in html.find_all("p")
                      if p.text != "\n"]
        return status_code, page_title, paragraphs
    return status_code, "NotFound", []


# p_title, ps = get_data_from_title("mathematicafgf")
# print(p_title)
# for p in ps:
#     print(p)
