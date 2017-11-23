import os
os.environ['KERAS_BACKEND']='tensorflow'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import keras.backend as K
K.set_image_dim_ordering('tf')

import cv2
import keras
from keras.utils import plot_model
from keras.applications.imagenet_utils import preprocess_input
from keras.backend.tensorflow_backend import set_session
from keras.models import Model
from keras.preprocessing import image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread
import tensorflow as tf

from ssd import SSD300
from ssd_utils import BBoxUtility

# %matplotlib inline
plt.rcParams['figure.figsize'] = (8, 8)
plt.rcParams['image.interpolation'] = 'nearest'

np.set_printoptions(suppress=True)

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.45
set_session(tf.Session(config=config))

# voc_classes = ['Aeroplane', 'Bicycle', 'Bird', 'Boat', 'Bottle',
#                'Bus', 'Car', 'Cat', 'Chair', 'Cow', 'Diningtable',
#                'Dog', 'Horse','Motorbike', 'Person', 'Pottedplant',
#                'Sheep', 'Sofa', 'Train', 'Tvmonitor']

voc_classes = ['adidas',
 'aldi',
 'apple',
 'becks',
 'bmw',
 'carlsberg',
 'chimay',
 'cocacola',
 'corona',
 'dhl',
 'erdinger',
 'esso',
 'fedex',
 'ferrari',
 'ford',
 'fosters',
 'google',
 'guiness',
 'heineken',
 'HP',
 'lays',
 'milka',
 'nvidia',
 'paulaner',
 'pepsi',
 'rittersport',
 'shell',
 'singha',
 'starbucks',
 'stellaartois',
 'texaco',
 'tsingtao',
 'ups',
 'yili',
 'keaiduo',
 'magnum',
 'heluxue',
 'DAVIDOFF',
 'BURGERKING',
 'ef',
 'minute_en',
 'chuncui',
 'eddge',
 'minute_zh',
 'Anchor',
 'shengdanbei',
 'aeroplane',
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
 'tvmonitor',
 'chinatelecom',
 'mengniu',
 'listerine',
 'chinaunicom',
 'haier',
 'qiangsheng',
 'safeguard',
 'dove',
 'vaseline',
 'chanel',
 'nongfushanquan',
 'chinamobile',
 'skii',
 'huawei',
 'xinxiangyin',
 'haifeisi',
 'midea',
 'zhaohang',
 'gree',
 'lipton',
 'budweiser',
 'harbinbeer',
 'yeehoo',
 'Jia Duo Bao',
 'wanglaoji',
 'mirinda',
 'heytea',
 'tongyi',
 'red bull',
 'sprite',
 'mizone',
 'fanta',
 'weiquan',
 'vita',
 'kangshifu',
 'wushilan',
 'yidiandian',
 'ambrosial']

NUM_CLASSES = len(voc_classes) + 1

input_shape=(300, 300, 3)
model = SSD300(input_shape, num_classes=NUM_CLASSES)
model.load_weights('./checkpoints/weights.19.hdf5', by_name=True)
bbox_util = BBoxUtility(NUM_CLASSES)

plot_model(model, show_shapes=True)

inputs = []
images = []

fpath = './background'
all_files = os.listdir(fpath)

for f in all_files:
    img_path = os.path.join(fpath, f)
    print img_path
    img = image.load_img(img_path, target_size=(300, 300))
    img = image.img_to_array(img)
    images.append(imread(img_path))
    inputs.append(img.copy())

inputs = preprocess_input(np.array(inputs))

preds = model.predict(inputs, batch_size=1, verbose=1)

results = bbox_util.detection_out(preds)

# %%time
a = model.predict(inputs, batch_size=1)
b = bbox_util.detection_out(preds)

for i, img in enumerate(images):
    # Parse the outputs.
    det_label = results[i][:, 0]
    det_conf = results[i][:, 1]
    det_xmin = results[i][:, 2]
    det_ymin = results[i][:, 3]
    det_xmax = results[i][:, 4]
    det_ymax = results[i][:, 5]

    # Get detections with confidence higher than 0.6.
    top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.6]

    top_conf = det_conf[top_indices]
    top_label_indices = det_label[top_indices].tolist()
    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]

    colors = plt.cm.hsv(np.linspace(0, 1, len(voc_classes)+1)).tolist()

    plt.imshow(img / 255.)
    currentAxis = plt.gca()

    for i in range(top_conf.shape[0]):
        xmin = int(round(top_xmin[i] * img.shape[1]))
        ymin = int(round(top_ymin[i] * img.shape[0]))
        xmax = int(round(top_xmax[i] * img.shape[1]))
        ymax = int(round(top_ymax[i] * img.shape[0]))
        score = top_conf[i]
        label = int(top_label_indices[i])
        label_name = voc_classes[label - 1]
        display_txt = '{:0.2f}, {}'.format(score, label_name)
        coords = (xmin, ymin), xmax - xmin + 1, ymax - ymin + 1
        color = colors[label]
        currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
        currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor': color, 'alpha': 0.5})

    plt.show()