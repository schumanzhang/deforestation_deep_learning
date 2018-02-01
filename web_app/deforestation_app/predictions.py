from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import numpy as np
from keras.models import Sequential
from keras.preprocessing import image
from tqdm import tqdm
from PIL import ImageFile                            
ImageFile.LOAD_TRUNCATED_IMAGES = True 

def upload_to(filename):
    return 'images/{}'.format(filename)

class ImageUpload(models.Model):
    
    image = models.ImageField(_('image'), blank=True, null=True, upload_to=upload_to)
    modelName = models.CharField(_('modelName'), max_length=100)
    
class CNN_Prediction(object):
    
    def __init__(self):
        self.cnn_model = Sequential()
        self.cnn_model.load_weights('saved_models/weights.best.ResNet50_deep.hdf5')
        #needs to actually build this
        
    def process_images(self):
        image_files = np.array(['images/test_0.jpg', 'images/test_1.jpg'])
        tensors = self.paths_to_tensor(image_files).astype('float32')/255
        return tensors
        
    def path_to_tensor(self, img_path):
        img = image.load_img(img_path, target_size=(256, 256))
        x = image.img_to_array(img)
        return np.expand_dims(x, axis=0)

    def paths_to_tensor(self, img_paths):
        list_of_tensors = [self.path_to_tensor(img_path) for img_path in tqdm(img_paths)]
        return np.vstack(list_of_tensors)
    
    def predict_image(self, tensors):
        predictions = []
        for tensor in tensors:
            result = self.cnn_model.predict(np.expand_dims(tensor, axis=0))
            preds = result[0]
            preds[preds >= 0.5] = 1
            preds[preds < 0.5] = 0 
            predictions.append(preds)

        return predictions