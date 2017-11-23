# -*- coding:utf-8 -*-
from keras.preprocessing.image import img_to_array, load_img
from pascal_voc_io import PascalVocWriter
from pascal_voc_io import PascalVocReader
import re

import os
img_path='/media/wac/backup1/test_ssd/background/'
save_path='/media/wac/backup1/test_ssd/tmp'
R=re.compile('(\.jpg|\.jpeg|\.bmp|\.png|\.JPG)$')

for root,dirs ,files in os.walk(img_path):
    if len(files) == 0:
        continue
    for filename in files:
        if R.search(filename) !=None:
            abspath=os.path.join(root,filename)
            label=root.split('/')[-1]
            path=os.path.join(save_path,label)
            if not os.path.exists(path):
                os.mkdir(path)
            img=load_img(abspath)
            img=img_to_array(img)

            writer = PascalVocWriter('tests', filename[:-4], img.shape, localImgPath=abspath)
            difficult = 0
            name='background'


            writer.addBndBox(0, 0, img.shape[1],img.shape[0] , name, difficult)
            savename=os.path.join(path,filename)
            savename=savename[:-4]
            print savename
            writer.save('{}.xml'.format(str(savename)))

