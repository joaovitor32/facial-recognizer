import inquirer
import random
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

def cross_validation(comparing_function,train_images_splited,test_images_splited):
    correct = 0
    error = 0

    for img in test_images_splited_joined:
        picked_img = pimg.imread(input_data['PATH'] + img)
        
        diff,group,result = comparing_function(picked_img,train_images_splited)
        if define_class(img) == define_class(group):
            correct = correct + 1
        else:
            error = error + 1

        f, (plt0, plt1) = plt.subplots(1, 2, figsize=(10,5))
        plt0.imshow(picked_img)
        plt1.imshow(result)
        plt.show()
        
    return error,correct

def split_set(imgs):
    test_set = []

    for key in imgs:
        randomImg = random.choice(list(imgs[key]))
        test_set.append(randomImg)
        imgs[key].remove(randomImg)
    
    return imgs,test_set    
  

'''
Teste set -> ['87-2.jpg', '16-2.jpg', '15-2.jpg', '11-2.jpg', '2-2.jpg']
Train set -> {'2': ['2-1.jpg'], '11': ['11-1.jpg'], '15': ['15-1.jpg'], '16': ['16-1.jpg'], '87': ['87-1.jpg']}
'''
def recognition(imgs,comparing_function):
    imgs,test_set = split_set(imgs)
    print(imgs,test_set)
    return
    for i in range(input_data['NUM_ITER']):
        error,correct = cross_validation(comparing_function,train_images_splited,test_images_splited)
        print("Porcentagem de acerto:",correct/(error+correct))

if __name__ == '__main__':

 
    input_data = yaml_data()

    method_map = {
        'Brute': brute_force_comparison,
        'PCA': pca_comparison,
    }

    imgs = load_images()
    formatted_images = format_images(imgs)   

    main=True
    options = [['Sim',True],['Não',False]]
    methods = ['PCA','Brute']
    while main:
        try:
            question = [inquirer.List('prompt',message="Deseja continuar?",choices=[options[0][0],options[1][0]])]
            main = options[[i[0] for i in options].index(inquirer.prompt(question)['prompt'])][1]

            if not main:
                break

            method_list = [inquirer.List('prompt',message="Qual método?",choices=[methods[0],methods[1]])]
            choosed_method = methods[[i for i in methods].index(inquirer.prompt(method_list)['prompt'])]

            comparing_function = method_map[choosed_method]
            recognition(formatted_images,comparing_function)

        except KeyboardInterrupt:
            print("\n Algm erro aparentemente aconteceu")
            sys.exit(0)
