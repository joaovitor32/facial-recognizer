import inquirer
import random
import copy
import time
import sys
import os, os.path
from PIL import Image
import matplotlib.image as pimg
import matplotlib.pyplot as plt
from libs.yaml.main import yaml_data
from libs.PCA.main import pca_comparison
from utils.define_class.main import define_class
from sklearn.model_selection import train_test_split
from libs.Brute_Force.main import brute_force_comparison

'''
    Function that loads images from specific folder
'''
def load_images():
    imgs = []
    valid_images = [input_data['EXT']]
    for f in os.listdir(input_data['PATH']):
        name=os.path.splitext(f)
        ext = name[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append([name[0],Image.open(os.path.join(input_data['PATH'],f))])
    
    return imgs 


'''
    Separate the image names into subclasses=> [1-1,1-2.1-2] => [1,[1,2,3]] ->
    Dictionary being used
'''
def format_images(imgs): 
    subclass={}

    for filename,img in imgs:
        name_img = filename.split("-")[0]
        subclass_img = filename.split("-")[1]

        if subclass.__contains__(name_img):
            subclass[name_img]={*subclass[name_img],name_img+"-"+subclass_img+input_data['EXT']}
        else:
            subclass[name_img]={name_img+"-"+subclass_img+input_data['EXT']}

    return subclass


def split_set(imgs):
    test_set = []

    train_set = copy.deepcopy(imgs)

    for key in train_set:
        randomImg = random.choice(list(train_set[key]))
        test_set.append(randomImg)
        train_set[key].remove(randomImg)
    
    return train_set,test_set    

'''
    Cross-validation of the image set
'''
def cross_validation(iter,comparing_function,train_set,test_set):
    correct = 0
    error = 0

    for img in test_set:
        picked_img = pimg.imread(input_data['PATH'] + img)    
        diff,group,result = comparing_function(picked_img,train_set)
    
        result_comparison = define_class(img) == group
        if result_comparison:
            correct = correct + 1
        else:
            error = error + 1

        if input_data['SHOW_IMAGES']:
            f, (fig1, fig2) = plt.subplots(1, 2, figsize=(10,5))
            f.suptitle("Iteration: {}, Result of comparison: {}".format(iter,result_comparison))
            fig1.imshow(picked_img)
            fig2.imshow(result)
            plt.pause(input_data['TIME_BETWEEN_IMAGES'])
            plt.close()
            plt.show()
    
    return (correct*100.)/(correct+error)

'''
Teste set -> ['87-2.jpg', '16-2.jpg', '15-2.jpg', '11-2.jpg', '2-2.jpg']
Train set -> {'2': ['2-1.jpg'], '11': ['11-1.jpg'], '15': ['15-1.jpg'], '16': ['16-1.jpg'], '87': ['87-1.jpg']}
'''
def recognition(imgs,comparing_function):

    tax = 0
    num_iter = input_data['NUM_ITER']

    for iter in range(num_iter):
        train_set,test_set = split_set(imgs)
        tax = tax + cross_validation(iter,comparing_function,train_set,test_set) 
        print("Iteração: {0} da etapa de reconhecimento. Percentual parcial: {1}% ".format(iter,tax/num_iter),end="\r")                                   
        time.sleep(0.1)    
    
    print("\nTaxa de acerto final: {}%".format(tax/num_iter))
    

if __name__ == '__main__':

    input_data = yaml_data()

    method_map = {
        'Brute': brute_force_comparison,
        'PCA': pca_comparison,
    }

    imgs = load_images()
    formatted_images = format_images(imgs)   

    comparing_function = method_map[input_data['METHOD']]
    recognition(formatted_images,comparing_function)
