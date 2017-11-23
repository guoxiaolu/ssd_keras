import numpy as np
import os
from xml.etree import ElementTree

class XML_preprocessor(object):

    def __init__(self, data_path, label_names):
        self.path_prefix = data_path
        self.label_names = label_names
        self.num_classes = len(label_names)
        self.data = dict()
        self._preprocess_XML()

    def _preprocess_XML(self):
        filenames = os.listdir(self.path_prefix)
        for filename in filenames:
            if os.path.splitext(filename)[1] != '.xml':
                continue
            tree = ElementTree.parse(self.path_prefix + filename)
            root = tree.getroot()
            bounding_boxes = []
            one_hot_classes = []
            size_tree = root.find('size')
            width = float(size_tree.find('width').text)
            height = float(size_tree.find('height').text)
            for object_tree in root.findall('object'):
                for bounding_box in object_tree.iter('bndbox'):
                    xmin = float(bounding_box.find('xmin').text)/width
                    ymin = float(bounding_box.find('ymin').text)/height
                    xmax = float(bounding_box.find('xmax').text)/width
                    ymax = float(bounding_box.find('ymax').text)/height
                bounding_box = [xmin,ymin,xmax,ymax]
                bounding_boxes.append(bounding_box)
                class_name = object_tree.find('name').text
                one_hot_class = self._to_one_hot(class_name)
                one_hot_classes.append(one_hot_class)
            # image_name = root.find('filename').text
            image_name = os.path.splitext(filename)[0] + '.jpg'
            bounding_boxes = np.asarray(bounding_boxes)
            one_hot_classes = np.asarray(one_hot_classes)
            image_data = np.hstack((bounding_boxes, one_hot_classes))
            self.data[image_name] = image_data

    def _to_one_hot(self,name):
        one_hot_vector = [0] * self.num_classes
        if name in self.label_names:
            index = self.label_names.index(name)
            one_hot_vector[index] = 1
        else:
            print('unknown label: %s' %name)

        return one_hot_vector

# example on how to use it
# all_names = ['adidas',
#  'aldi',
#  'apple',
#  'becks',
#  'bmw',
#  'carlsberg',
#  'chimay',
#  'cocacola',
#  'corona',
#  'dhl',
#  'erdinger',
#  'esso',
#  'fedex',
#  'ferrari',
#  'ford',
#  'fosters',
#  'google',
#  'guiness',
#  'heineken',
#  'HP',
#  'lays',
#  'milka',
#  'nvidia',
#  'paulaner',
#  'pepsi',
#  'rittersport',
#  'shell',
#  'singha',
#  'starbucks',
#  'stellaartois',
#  'texaco',
#  'tsingtao',
#  'ups',
#  'yili',
#  'keaiduo',
#  'magnum',
#  'heluxue',
#  'DAVIDOFF',
#  'BURGERKING',
#  'ef',
#  'minute_en',
#  'chuncui',
#  'eddge',
#  'minute_zh',
#  'Anchor',
#  'shengdanbei',
#  'aeroplane',
#  'bicycle',
#  'bird',
#  'boat',
#  'bottle',
#  'bus',
#  'car',
#  'cat',
#  'chair',
#  'cow',
#  'diningtable',
#  'dog',
#  'horse',
#  'motorbike',
#  'person',
#  'pottedplant',
#  'sheep',
#  'sofa',
#  'train',
#  'tvmonitor',
#  'chinatelecom',
#  'mengniu',
#  'listerine',
#  'chinaunicom',
#  'haier',
#  'qiangsheng',
#  'safeguard',
#  'dove',
#  'vaseline',
#  'chanel',
#  'nongfushanquan',
#  'chinamobile',
#  'skii',
#  'huawei',
#  'xinxiangyin',
#  'haifeisi',
#  'midea',
#  'zhaohang',
#  'gree',
#  'lipton',
#  'budweiser',
#  'harbinbeer',
#  'yeehoo',
#  'Jia Duo Bao',
#  'wanglaoji',
#  'mirinda',
#  'heytea',
#  'tongyi',
#  'red bull',
#  'sprite',
#  'mizone',
#  'fanta',
#  'weiquan',
#  'vita',
#  'kangshifu',
#  'wushilan',
#  'yidiandian',
#  'ambrosial',
#  'background']
all_names = ['aeroplane',
 'bicycle',
 'bird',
 'boat',
 'bottle',
 'bus',
 'car',
 'cat',
 'chair',
 'cow',
 'diningtable',
 'dog',
 'horse',
 'motorbike',
 'person',
 'pottedplant',
 'sheep',
 'sofa',
 'train',
 'tvmonitor']

import pickle
data = XML_preprocessor('/Users/Lavector/dataset/VOC2012/Annotations/', all_names).data
pickle.dump(data,open('../VOC2012.pickle','wb'))

