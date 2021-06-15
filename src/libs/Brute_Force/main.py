from utils.compare_images.main import compare_images
import matplotlib.image as pimg

from libs.yaml.main import yaml_data

'''
    Compare an image to test images
    according to your class via Brute Force - Cross Comparison
    Distance by normalization
'''
def brute_force_comparison(img,train_images):
    input_data = yaml_data()

    result = []
    diff= input_data['AUX']
    group = ''
    for img_train in train_images:
        for selected_img in train_images[train_images.index(img_train)][1]:
            img_compare =  pimg.imread(input_data['PATH'] + selected_img)
      
            dist = compare_images(img[:, :, 0:3] , img_compare[:, :, 0:3])
            if dist<diff:
                diff = dist
                result = img_compare
                group = img_train[0]   

    return diff,group,result