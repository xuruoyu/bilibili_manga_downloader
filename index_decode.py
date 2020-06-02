import io
import os
from pprint import pprint
import numpy as np
import zipfile
import json


def decode_index_data(season_id: int, episode_id: int, buf):
    u = [66, 73, 76, 73, 67, 79, 77, 73, 67]
    l = len(u)
    e = buf[l:]
    # print(buf)
    _e = []
    for i in range(len(e)):
        _e.append(e[i])
    e = np.uint8(_e)
    # print(e)
    n = [0, 0, 0, 0, 0, 0, 0, 0]
    n = np.array(n, dtype='uint8')
    n[0] = episode_id
    n[1] = episode_id >> 8
    n[2] = episode_id >> 16
    n[3] = episode_id >> 24
    n[4] = season_id
    n[5] = season_id >> 8
    n[6] = season_id >> 16
    n[7] = season_id >> 24
    # print(n)
    _n = 0
    r = len(e)
    while _n < r:
        e[_n] = e[_n] ^ n[_n % 8]
        _n = _n + 1
        pass
    # print("解密后：")
    # print(e)
    ret = bytes(e)
    # print(ret)
    z = zipfile.ZipFile(io.BytesIO(ret), 'r')
    j = z.read('index.dat')
    # print(j)
    # pprint(json.loads(j)['pics'])
    return json.loads(j)['pics']
    pass


if __name__ == "__main__":
    season_id = 25966
    episode_id = 376715
    f = open('data.index.28227a12', 'rb')
    buf = f.read()
    f.close()
    print(len(buf))
    decode_index_data(season_id, episode_id, buf)
    pass
