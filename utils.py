# coding: utf-8
from numpy import array
from PIL import Image

def do_image_crop(img):
    """做图片切割，返回块图片列表"""
    start = 20
    width = 35
    top = 0
    height = 100

    img_list = []

    def init_table(threshold=135):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        return table

    img = img.convert("L").point(init_table(), '1')
    #img.save('result.jpg')

    for i in range(4):
        new_start = start + width * i
        box = (new_start, top, new_start + width, height)
        piece = img.crop(box)
        #print(type(piece))
        #piece.save(str(i)+".jpg")
        img_list.append(piece)

    return img_list


def img_list_to_array_list(img_list):
    """PIL Image对象转array_list"""
    array_list = []
    for img in img_list:
        array_list.append(array(img).flatten())
    return array_list


if __name__=="__main__":
    #r = requests.get("http://cet.neea.edu.cn/imgs/1b350fc9f7ab4177aebf82fca2311a11.png")
    img = Image.open('45548942e5844ed39467e09e782d0e2e.png')
    do_image_crop(img)
    #code = get_validate_code_from_image(img)
    #print(code)
