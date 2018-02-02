'''
from rest_framework.serializers import HyperlinkedModelSerializer

from deforestation_app.predictions import ImageUpload

class ImageUploadSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('modelname', 'image')
        readonly_fields = ('image')
'''