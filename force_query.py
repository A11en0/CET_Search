# coding: utf-8
"""
暴力查询模块
1. 根据输入的前10为准考证号，暴力破解后5为准考证号（考场号3位 + 座位号2位）
2. 指定准考证号ID获取指定验证码图片
3. 图片输入机器学习模块，获取验证码值
4. 提交验证码进行查询，获取相应的结果：验证码错误/无结果/非上述两者，查询成功


准考证号列表

a. 获取验证码
b. 提交查询请求
    如果成功：结束
    如果验证码错误：重新获取验证码并提交
    如果查询结果为空：生成新的准考证号并提交

"""
import os
import time
import random
import requests
import threading
from PIL import Image
from io import BytesIO
from get_images import get_image_url_and_filename
from settings import image_api, query_api, img_api_headers, query_api_headers
from validate_api import get_validate_code_from_image

myid = "5300601811{js:03d}{zw:02d}"
name = "李柏翰"

NETWORK_STATUS = True

cnt = 0
cnt_right = 0

'''
def log_info(*args):
    print("日志：", *args)
'''

def send_query_until_true(js, zw):
    global cnt
    # 生成准考证号
    new_id = myid.format(js=js, zw=zw)
    # 获取验证码图片地址
    img_api_url = image_api.format(id=new_id)
    img_api_resp = requests.get(img_api_url, headers=img_api_headers)
    img_url, filename = get_image_url_and_filename(img_api_resp.text)
    # 获取验证码图片并猜测
    img_resp = requests.get(img_url, stream=True)
    if img_resp.status_code == 200:
        code = get_validate_code_from_image(Image.open(BytesIO(img_resp.content)))
    else:
        # 404后直接赋值一个错误的code, 以便接下来递归回来
        code = "xxxx"

    # 执行查询操作
    cnt += 1
    data = {
        "data": "CET4_181_DANGCI,{id},{name}".format(id=new_id, name=name),
        "v": code
    }
    #log_info(data)
    print("Try: " + data['data'].split(',')[1] + "," +data['data'].split(',')[2])
#    threadLock.acquire()

    try:
        query_resp = requests.post(query_api, data=data, headers=query_api_headers, timeout=5)
        if query_resp.status_code == 200:
            query_text = query_resp.text
    except requests.exceptions.Timeout:
        global NETWORK_STATUS
        NETWORK_STATUS = False

        if NETWORK_STATUS == False:
            for i in range(1, 10):
                print("第%s次超时,正在重新请求."%i)
                query_resp = requests.post(query_api, data=data, headers=query_api_headers, timeout=5)
                if query_resp.status_code == 200:
                    query_text = query_resp.text
                    break
                
#    threadLock.release()        
    print("Result: " + query_text)
    

    
    if "验证码错误" in query_text:
        query_text = send_query_until_true(js, zw)
        '''
        if not os.path.exists("download_error_capture"):
            os.mkdir('download_error_capture')
        with open("download_error_capture/%s.png" % random.randint(10000, 99999), "wb") as f:
            f.write(img_resp.content)
            f.close()
        '''
    else:
        if not os.path.exists("download_capture"):
            os.mkdir('download_capture')
        with open("download_capture/%s.png" %code, "wb") as f:
            f.write(img_resp.content)
            f.close()

    return query_text

def main(start,end):
    global cnt_right
    for js in range(start, end):
        for zw in range(1, 30):
            query_text = send_query_until_true(js, zw)
            if "您查询的结果为空" in query_text:
                cnt_right += 1
                continue
            else:
                result = str(js) + str(zw)
                print("后五位是：%s" % result)
                with open('the_result.txt', 'a') as f:
                    f.write("后五位是：%s" % result + '\n')
                    f.close()
                os._exit(0)
                return True

    print("正确率: ", cnt_right/cnt*1.0)

    
threadLock = threading.Lock()
threads = []
d = 1 
for i in range(1,120):
    t = threading.Thread(target=main, args=(1+(i-1)*d, 2+(i-1)*d))  
    threads.append(t)

if __name__ == '__main__':
    start = time.time()
    #启动线程  
    for i in threads:  
        i.start()  
    #keep thread  
    for i in threads:  
        i.join()

