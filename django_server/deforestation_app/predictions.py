from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

import numpy as np
from keras.models import Sequential
from keras.preprocessing import image
from tqdm import tqdm
from PIL import ImageFile                            
ImageFile.LOAD_TRUNCATED_IMAGES = True 

from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.models import Model
from keras.applications.resnet50 import ResNet50
from keras.applications.xception import Xception
from keras.backend import clear_session

def upload_to(filename):
    return 'images/{}'.format(filename)

class ImageUpload(models.Model):
    
    image = models.ImageField(_('image'), blank=True, null=True, upload_to=upload_to)
    modelName = models.CharField(_('modelName'), max_length=100)
    
class CNN_Prediction(object):
    
    def __init__(self):
        self.classes = [
            'agriculture', 'bare_ground', 'blooming', 'blow_down', 'clear',
            'conventional_mine', 'cultivation', 'habitation', 'haze', 'partly_cloudy',
            'primary', 'road', 'selective_logging', 'slash_burn', 'water', 'cloudy', 'artisinal_mine'
        ]
        
    def build_ResNet50_Deep(self):
        base_model_Resnet50 = ResNet50(include_top=False, input_shape=(256, 256, 3), weights='imagenet')
        x = base_model_Resnet50.output
        x = GlobalAveragePooling2D()(x)
        predictions = Dense(len(self.classes), activation='sigmoid')(x)

        model = Model(base_model_Resnet50.input, predictions)
        model.load_weights('saved_models/weights.best.ResNet50_deep.hdf5')

        return model
    
    def build_ResNet50_Shallow(self):
        base_model_Resnet50 = ResNet50(include_top=False, input_shape=(256, 256, 3), weights='imagenet')
        x = base_model_Resnet50.output
        x = GlobalAveragePooling2D()(x)
        predictions = Dense(len(self.classes), activation='sigmoid')(x)

        model = Model(base_model_Resnet50.input, predictions)
        model.load_weights('saved_models/weights.best.ResNet50_shallow.hdf5')

        return model
    
    def build_Original(self):
        model = Sequential()
        model.add(Conv2D(filters=20, kernel_size=3, padding='valid', activation='relu', input_shape=(256, 256, 3)))
        model.add(MaxPooling2D(pool_size=2))
        model.add(Conv2D(filters=40, kernel_size=3, padding='valid', activation='relu'))
        model.add(MaxPooling2D(pool_size=2))
        model.add(Conv2D(filters=80, kernel_size=3, padding='valid', activation='relu'))
        model.add(MaxPooling2D(pool_size=2))

        model.add(Dropout(0.1))
        model.add(Flatten())
        model.add(Dense(len(self.classes), activation='sigmoid'))
        model.load_weights('saved_models/weights.best.from_original.hdf5')

        return model
    
    def build_Xception(self):
        base_model_Xception = Xception(include_top=False, input_shape=(256, 256, 3), weights='imagenet')
        x = base_model_Xception.output
        x = GlobalAveragePooling2D()(x)
        predictions = Dense(len(self.classes), activation='sigmoid')(x)

        model = Model(base_model_Xception.input, predictions)
        model.load_weights('saved_models/weights.best.Xception.hdf5')

        return model
        
    def process_images(self):
        image_files = np.array(['images/test_0.jpg', 'images/test_1.jpg', 'images/test_2.jpg'])
        tensors = self.paths_to_tensor(image_files).astype('float32')/255
        return tensors
    
    def process_image(self, filename):
        image_files = np.array(['images/' + filename])
        tensors = self.paths_to_tensor(image_files).astype('float32')/255
        return tensors
        
    def path_to_tensor(self, img_path):
        img = image.load_img(img_path, target_size=(256, 256))
        x = image.img_to_array(img)
        return np.expand_dims(x, axis=0)

    def paths_to_tensor(self, img_paths):
        list_of_tensors = [self.path_to_tensor(img_path) for img_path in tqdm(img_paths)]
        return np.vstack(list_of_tensors)
    
    def predict_image(self, selected_model, tensors):
        predictions = []
        for tensor in tensors:
            result = selected_model.predict(np.expand_dims(tensor, axis=0))
            preds = result[0]
            preds[preds >= 0.5] = 1
            preds[preds < 0.5] = 0 
            predictions.append(preds)

        return predictions
    
    def convert_prediction(self, predictions):
        labels = []
        for result in predictions:
            result_list = result.tolist()
            label = []
            for i in range(len(result_list)):
                if result_list[i] == 1:
                    label.append(self.classes[i])
                    
            labels.append(label)
            
        return labels
    
    def clear_models(self):
        clear_session()
    
    
    
    
    
    
    