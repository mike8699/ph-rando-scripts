from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
import numpy as np
from sklearn.cluster import KMeans
import shutil, glob, sys
from pathlib import Path
from PIL import Image as pil_image
image.LOAD_TRUNCATED_IMAGES = True 
model = VGG16(weights='imagenet', include_top=False)

# Variables
imdir = Path('E:\\phantom_hourglass\\ph\\scripts\\analyze_image\\screenshots_cropped')
targetdir = Path('E:\\phantom_hourglass\\ph\\scripts\\analyze_image\\screenshots_analyzed')
number_clusters = 9

# create the target directory if it doesn't exist
Path.mkdir(targetdir, parents=True, exist_ok=True)

# Loop over files and get features
filelist = glob.glob(f'{str(imdir)}/*.png')
filelist.sort()
featurelist = []
for i, imagepath in enumerate(filelist):
    print(f'    Status: {i} / {len(filelist)}', end='\r')
    img = image.load_img(imagepath, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    features = np.array(model.predict(img_data))
    featurelist.append(features.flatten())

# Clustering
kmeans = KMeans(n_clusters=number_clusters, random_state=0).fit(np.array(featurelist))

# Copy with cluster name
print("\n")
for i, m in enumerate(kmeans.labels_):
    Path.mkdir(targetdir / str(m), parents=True, exist_ok=True)
    print(f'    Copy: {i} / {len(kmeans.labels_)}', end='\r')
    shutil.copy(filelist[i], f'{(targetdir / str(m)) / (Path(filelist[i]).name)}')
