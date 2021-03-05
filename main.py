import json
import requests
from bs4 import BeautifulSoup



def get_script(doc):
    init_str = 'var ytInitialData'
    
    for s in doc.find_all('script'):
        text = str(s.string)
        if text is None:
            continue
                
        if text.startswith(init_str):
           return s

    return None


def get(url):
    url_template = f"https://www.youtube.com/channel/{url}/about"
    html_body = requests.get(url_template).text

    doc = BeautifulSoup(html_body, 'html.parser')
    return doc


def main():
    g = get('UCL7DDQWP6x7wy0O6L5ZIgxg')
    src = get_script(g)
    print(src.string[-50:])


if __name__ == "__main__":
    main()
