# coding: utf-8
"""
统计标记的图片字母数字分布频数
"""

import os
import pprint


'''
def get_filename_list():
    name = os.listdir("labeled_images")
    return name


def main():
    count_dct = {}
    name_list = get_filename_list()
    for name in name_list:
        #print(name[0:3])
        for word in name[0:4]:
            if word not in count_dct:
                count_dct[word] = 1
            else:
                count_dct[word] += 1

    print("总计字符：", len(count_dct))
    pprint.pprint(count_dct)
'''


def main():
    dir = 'train_images/'
    count_dct = {}
    charList = os.listdir(dir)
    for chr in charList:
        fileList = os.listdir(dir+chr)
        if chr not in count_dct:
            count_dct[chr] = len(fileList)
    print("Charater Total: ", len(charList))
    pprint.pprint(count_dct)

if __name__ == '__main__':
    main()
