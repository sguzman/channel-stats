import json
import requests
from bs4 import BeautifulSoup


init_str = 'var ytInitialData = '


def get_view(js):
    indexes = [
            'contents',
            'twoColumnBrowseResultsRenderer',
            'tabs',
            5,
            'tabRenderer',
            'content',
            'sectionListRenderer',
            'contents',
            0,
            'itemSectionRenderer',
            'contents',
            0,
            'channelAboutFullMetadataRenderer',
            'viewCountText',
            'simpleText'
    ]

    tmp = js
    for i in indexes:
       tmp = tmp[i]

    
    tmp = tmp.removesuffix(' views')
    tmp = tmp.replace(',', '')
    tmp = int(tmp)

    return tmp


def get_json(doc):
    text = str(doc.string)
    text = text.removeprefix(init_str)
    text = text.removesuffix(';')

    js = json.loads(text)

    return js


def get_script(doc):
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
    js = get_json(src)
    view = get_view(js)

    print(json.dumps(view, indent=4, sort_keys=True))



if __name__ == "__main__":
    main()
