from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import detail_route, parser_classes
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from deforestation_app.predictions import ImageUpload
from deforestation_app.predictions import CNN_Prediction
from deforestation_app.serializers import ImageUploadSerializer

class OriginalModel(APIView):
    
    def get(self, request):
        return Response({'Recall score': 0.69, 'Precision score': 0.82, 'Fbeta score': 0.70})
    
class ResNet50ModelShallow(APIView):
    
    def get(self, request):
        return Response({'Recall score': 0.79, 'Precision score': 0.85, 'Fbeta score': 0.80})
    
class ResNet50ModelDeep(APIView):
    
    def get(self, request):
        return Response({'Recall score': 0.83, 'Precision score': 0.89, 'Fbeta score': 0.84})

class XceptionModel(APIView):
    
    def get(self, request):
        return Response({'Recall score': 0.68, 'Precision score': 0.82, 'Fbeta score': 0.68})
    
class GetBestPrediction(APIView):    
    
    def get(self, request):
        cnn_model = CNN_Prediction()
        tensors = cnn_model.process_images()
        selected_model = cnn_model.build_ResNet50_Deep()
        predictions = cnn_model.predict_image(selected_model, tensors)
        labels = cnn_model.convert_prediction(predictions)
        return Response({'predictions': labels})

class GetImageUploadPredictionViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @detail_route(methods=['POST'])
    @parser_classes((FormParser, MultiPartParser))
    def predict(self, request, *args, **kwargs):
        print('request')
        print(request.data)
        if 'upload' in request.data:
            print('GetImageUploadPredictionViewSet')
            user_image = self.get_object()
            
            print(user_image)
            user_image.image.delete()
            
            upload = request.data['upload']
            print(upload)
            user_image.image.save(upload.name, upload)
            
            # send the prediction back with the image
            return Response(status=HTTP_201_CREATED, headers={'Location': user_image.image.url})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        
