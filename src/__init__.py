import os, os.path
from PIL import Image

ext = ".jpg"

#Function that loads images from specific folder
def load_images(path):
    imgs = []
    valid_images = [".jpg",".gif",".png",".tga"]
    for f in os.listdir(path):
        name=os.path.splitext(f)
        ext = name[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append([name[0],Image.open(os.path.join(path,f))])
    
    return imgs 


'''
Separar em subclasses o nome das imagens=> [1-1,1-2,1-2] => [1,[1,2,3]] -> 
Dictionary sendo Usado
'''

def format_images(imgs): 
    subclass={}
    for filename,img in imgs:
        name_img = filename.split("-")[0]
        subclass_img = filename.split("-")[1]

        if subclass.__contains__(name_img):
            subclass[name_img]={*subclass[name_img],name_img+"-"+subclass_img+ext}
        else:
            subclass[name_img]={name_img+"-"+subclass_img+ext}

    return subclass


if __name__ == '__main__':
    path = "data/recdev/easy/"
    imgs = load_images(path)
    formatted_images = format_images(imgs)   
    print(formatted_images) 
    #recognition(formatted_images)