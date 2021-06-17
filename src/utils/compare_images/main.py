from utils.normalize.main import normalize

def compare_images(img1, img2):

    diff = normalize(img1 - img2) 
    return diff
