import numpy
from PIL import Image
import json
def check_sameImg():
    im = Image.open(open('im1.jpg','rb'))
    array = numpy.array(im)
    # with open('imgarray.py','a') as fb:
    #     list = []
    #     list.append([111111111])
    #     list.append(array.tolist())
    #     fb.write(str(list))
    #     fb.write('\n')
    with open('imgarray.py','r') as fb:
        line = fb.readline()

        while line:
            list = json.loads(line)
            list = list[1]
            line = fb.readline()
            isSameImg = True
            for i in range(len(array)):
                for j in range(len(array[0])):
                    if ((array[i, j] >= 245 and list[i][j] < 245) or (array[i, j] < 245 and list[i][j] >= 245)) and abs(list[i][j] - array[i, j]) > 10 :
                        isSameImg = False
            if isSameImg == True:
                print("有两张图片相同，不需要存储图片")
                break
        if isSameImg == False:
            print("有图片不相同，需要存储图片")
            with open('imgarray.py', 'a') as fb:
                list = []
                list.append([111111111])
                list.append(array.tolist())
                fb.write(str(list))
                fb.write('\n')
if __name__ == '__main__':
    check_sameImg()