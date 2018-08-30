# coding: utf-8
import os
import time
import requests
from PIL import Image
from io import BytesIO
from learn_images import get_classifier_from_learn
from utils import *

from get_images import get_image_url_and_filename
from settings import image_api, query_api, img_api_headers, query_api_headers

from sklearn.externals import joblib

def get_validate_code_from_image(img):
    img_piece = do_image_crop(img)
    X = img_list_to_array_list(img_piece)
    clf = joblib.load('clf0')
    #clf = get_classifier_from_learn()
    y = clf.predict(X)
    return "".join(y)


def get_image_url(num):
    url = 'http://cache.neea.edu.cn/Imgs.do?c=CET&ik={num}&t=0.6900761558030022'
    headers = {
        "Host": "cache.neea.edu.cn",                                     "Proxy-Connection": "keep-alive",                                "Pragma": "no-cache",                                            "Cache-Control": "no-cache",                                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
        "Accept": "*/*",                                                 "DNT": "1",                                                      "Referer": "http://cet.neea.edu.cn/cet/",                        "Accept-Encoding": "gzip, deflate",                              "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",                    "Cookie": "UM_distinctid=15ddab8ea07302-04182c5cab6868-791238-1fa400-15ddab8ea0976; BIGipServercache.neea.edu.cn_pool=2577451018.39455.0000; verify=enc|ba3633d8066b323cd1e4139c90a0f5ea84ca7e0112463eecd718e0949306c91f; Hm_lvt_dc1d69ab90346d48ee02f18510292577=1503370065,1503371098,1503372217,1503372362; Hm_lpvt_dc1d69ab90346d48ee02f18510292577=1503372362"                           }
    new_url = url.format(num=num)
    id = requests.get(url=new_url, headers=headers, timeout=5)
    if id.status_code == 200:
        image_href = id.text.split('/')[-1][:-3]
        return image_href
    else:
        print("获取图片url失败.")
        return False

if __name__ == '__main__':

    start = time.time()
    for i in range(50):

        image_href = get_image_url(530060181100101)
        url = "http://cet.neea.edu.cn/imgs/{href}".format(href=image_href)
        img = requests.get(url)

        '''
        # 获取验证码图片地址
        img_api_url = image_api.format(id=530060181100101)
        img_api_resp = requests.get(img_api_url, headers=img_api_headers)
        img_url, filename = get_image_url_and_filename(img_api_resp.text)
        # 获取验证码图片并猜测
        img = requests.get(img_url, stream=True)
        '''

        image = Image.open(BytesIO(img.content))
        code = get_validate_code_from_image(image)
        print(code)

    print("Time:", time.time() - start)

    '''
    fileList = os.listdir('download_capture')
    count = 0
    for li in fileList:
        print(li[:4])
        img = Image.open('download_capture/%s' % li)
        code = get_validate_code_from_image(img)
        print(code)
        if( code == li[:4] ):
            count += 1
            print("success -->", code)
        else:
            print("fail.")
    #print(count)
    print("正确率:", count/len(fileList)*1.0)
    '''



