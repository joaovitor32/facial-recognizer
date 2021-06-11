import sklearn.decomposition as decomp

def PCA(x):
    x = x.reshape(300,100)
    pca = decomp.PCA(n_components=2)
    pca.fit(x)
    return pca.transform(x)