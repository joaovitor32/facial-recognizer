import os, os.path
from PIL import Image
import inquirer
from sklearn.model_selection import train_test_split
import matplotlib.image as pimg

from libs.Brute_Force.main import brute_force_comparison
from libs.yaml.main import yaml_data

from utils.define_class.main import define_class

#Function that loads images from specific folder
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

def cross_validation(method,train_images_splited,test_images_splited):
    correct = 0
    error = 0
    '''
        Grouping test images in same array: [('87', {'87-5.jpg', '87-7.jpg'}), ('15', {'15-1.jpg', '15-4.jpg'})]=>['87-5.jpg', '87-7.jpg','15-1.jpg', '15-4.jpg']
    '''
    dataset=train_images_splited+test_images_splited

    test_images_splited_joined=[]
    for dict_img in dataset:
        for elem in dict_img[1]:
            test_images_splited_joined.append(elem)   

    for img in test_images_splited_joined:
        picked_img = pimg.imread(input_data['PATH'] + img)
        
        diff,group,result = brute_force_comparison(picked_img,train_images_splited)
        if define_class(img) == define_class(group):
            correct = correct + 1
        else:
            error = error + 1
        #plotar imagens com matplotlib Imagem e imagem comparada
        
    return error,correct

def recognition(imgs,method):
    for i in range(input_data['NUM_ITER']):
        train_images_splited, test_images_splited = train_test_split(list(imgs.items()), test_size=0.4,shuffle=True)
        error,correct = cross_validation(method,train_images_splited,test_images_splited)
        #print("Erro: ",error)
        #print("Acerto: ",correct)
        #print("Porcentagem:",correct/(error+correct))

if __name__ == '__main__':

 
    input_data = yaml_data()

    imgs = load_images()
    formatted_images = format_images(imgs)   

    main=True
    options = [['Sim',True],['Não',False]]
    methods = [['PCA'],['Bruto']]
    while main:
        try:
            question = [inquirer.List('prompt',message="Deseja continuar?",choices=[options[0][0],options[1][0]])]
            main = options[[i[0] for i in options].index(inquirer.prompt(question)['prompt'])][1]

            if not main:
                break

            method_list = [inquirer.List('prompt',message="Qual método?",choices=[methods[0],methods[1]])]
            choosed_method = methods[[i for i in methods].index(inquirer.prompt(method_list)['prompt'])][0]
            recognition(formatted_images,choosed_method)

        except KeyboardInterrupt:
            print("\n Algm erro aparentemente aconteceu")
            sys.exit(0)
