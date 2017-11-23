# -*- coding: utf-8 -*-
import os
import shutil
import random

img_path = '/media/wac/backup1/test_ssd/background'
dst_path = '/media/wac/backup1/test_ssd/tmp'
if not os.path.exists(dst_path):
    os.mkdir(dst_path)
fname = os.listdir(img_path)
i = 0
for f in fname:
    name = os.path.splitext(f)
    if name[1] == '.xml':
        i += 1
        new_name = 'background%d'%(i)
        shutil.copy(os.path.join(img_path, f), os.path.join(dst_path, new_name + '.xml'))
        shutil.copy(os.path.join(img_path, name[0] + '.jpg'), os.path.join(dst_path, new_name + '.jpg'))
