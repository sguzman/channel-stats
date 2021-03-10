from bs4 import BeautifulSoup
import concurrent
import concurrent.futures as futures
import grpc
import json
import logging
import requests

import lib
import lib.server_pb2 as server_pb2
import lib.server_pb2_grpc as server_pb2_grpc
import lib.log


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


def grab(arg):
    g = get(arg)
    src = get_script(g)
    js = get_json(src)
    view = get_view(js)

    return view


def port():
    import os

    return int(os.environ['PORT'])


def main():
    p = port()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    server_pb2_grpc.add_ViewsServicer_to_server(Server(), server)
    server.add_insecure_port(f'[::]:{p}')
    server.start()
    logging.info(f'Started server at {p}')
    server.wait_for_termination()


class Server(server_pb2_grpc.ViewsServicer):
    def view(self, request, context):
        name = grab(request.name)
        logging.info(name)
        return server_pb2.ChannelViews(views=name)


if __name__ == '__main__':
    main()
