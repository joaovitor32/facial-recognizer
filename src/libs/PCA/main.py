import math
import matplotlib.image as pimg
from libs.yaml.main import yaml_data
import sklearn.decomposition as decomp
from utils.compare_images.main import compare_images

'''
    Calculates the pca of the passed image as a parameter 
    but first resizes it from [100][100][3] to [300][100]
'''

def PCA(x):
    x = x.reshape(300,100)
    pca = decomp.PCA(n_components=2)
    pca.fit(x)
    return pca.transform(x)

'''
    Compare an image with test images from
    according to your class via PCA - Cross Comparison
    Distance by normalization
'''
def pca_comparison(img,train_images):
    input_data = yaml_data()

    result = []
    diff= input_data['AUX']
    group = 0
    for img_train in train_images:
        for selected_img in train_images[img_train]:
            img_compare =  pimg.imread(input_data['PATH'] + selected_img)
            dist = compare_images(PCA(img[:,:,0:3]),PCA(img_compare[:,:,0:3]))
    
            if dist<diff:
                diff = dist
                result = img_compare
                group = img_train

    return dist,group,result