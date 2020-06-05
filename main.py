import os
import time

import requests
import json
from pprint import pprint
from index_decode import decode_index_data

download_path = './manhua'
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://manga.bilibili.com",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "cookie": ""
}
headers_cdn = {
    'Host': 'manga.hdslb.com',
    'Origin': 'https://manga.bilibili.com',
}


def download_manga_all(comic_id: int):
    url = "https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web"
    res = requests.post(url,
                        json.dumps({
                            "comic_id": comic_id
                        }), headers=headers)
    data = json.loads(res.text)['data']
    comic_title = data['title']
    root_path = os.path.join(download_path, comic_title)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    for ep in data['ep_list']:
        if not ep['is_locked']:
            print('downloading ep:', ep['short_title'], ep['title'])
            download_manga_episode(ep['id'], root_path)
            pass
        pass
    pass


def download_manga_episode(episode_id: int, root_path: str):
    res = requests.post('https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisode?device=pc&platform=web',
                        json.dumps({
                            "id": episode_id
                        }), headers=headers)
    data = json.loads(res.text)
    # comic_title = data['data']['comic_title']
    short_title = data['data']['short_title']
    # title = comic_title + '_' + short_title + '_' + data['data']['title']
    title = short_title + '_' + data['data']['title']
    comic_id = data['data']['comic_id']
    print('正在下载：', title)

    # 获取索引文件cdn位置
    res = requests.post('https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web',
                        json.dumps({
                            "ep_id": episode_id
                        }), headers=headers)
    data = json.loads(res.text)
    index_url = 'https://manga.hdslb.com' + data['data']['path']
    print('获取索引文件cdn位置:', index_url)
    # 获取索引文件
    res = requests.get(index_url)
    # 解析索引文件
    pics = decode_index_data(comic_id, episode_id, res.content)
    # print(pics)
    ep_path = os.path.join(root_path, title)
    if not os.path.exists(ep_path):
        os.makedirs(ep_path)
    for i, e in enumerate(pics):
        url = get_image_url(e)
        print(i, e)
        res = requests.get(url)
        with open(os.path.join(ep_path, str(i) + '.jpg'), 'wb+') as f:
            f.write(res.content)
            pass
        if i % 4 == 0 and i != 0:
            time.sleep(2)
            pass
        pass
    pass


def get_image_url(img_url):
    # 获取图片token
    res = requests.post('https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web',
                        json.dumps({
                            "urls": json.dumps([img_url])
                        }), headers=headers)
    data = json.loads(res.text)['data'][0]
    url = data['url'] + '?token=' + data['token']
    return url
    pass


if __name__ == "__main__":
    download_manga_all(25966)
    # download_manga_episode(448369, os.path.join(download_path, '辉夜大小姐想让我告白 ~天才们的恋爱头脑战~'))
    # get_image_url('/bfs/manga/f311955085404cab705e881d0a81204098967c1e.jpg')
    pass
