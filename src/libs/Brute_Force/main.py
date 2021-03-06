import math
import matplotlib.image as pimg
from libs.yaml.main import yaml_data
from utils.compare_images.main import compare_images

'''
    Compare an image to test images
    according to your class via Brute Force - Cross Comparison
    Distance by normalization
'''
def brute_force_comparison(img,train_images):
    input_data = yaml_data()

    result = []
    diff= input_data['AUX']

    group = 0
    for img_train in train_images:
        for selected_img in train_images[img_train]:
            img_compare =  pimg.imread(input_data['PATH'] + selected_img)

            dist = compare_images(img[:, :, 0:3] , img_compare[:, :, 0:3])
            if dist<diff:
                diff = dist
                result = img_compare
                group = img_train  

    return diff,group,result