from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django import forms

from rest_framework.decorators import detail_route, parser_classes, list_route
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet

from deforestation_app.predictions import CNN_Prediction

'''
class IsAdminOrIsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff or request.user.is_superuser
'''

def handle_uploaded_file(f, filename):
    with open('images/' + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class OriginalModel(APIView):
    
    def get(self, request):
        return Response({'Recall_score': 0.69, 'Precision_score': 0.82, 'Fbeta_score': 0.70})
    
class ResNet50ModelShallow(APIView):
    
    def get(self, request):
        return Response({'Recall_score': 0.79, 'Precision_score': 0.85, 'Fbeta_score': 0.80})
    
class ResNet50ModelDeep(APIView):
    
    def get(self, request):
        return Response({'Recall_score': 0.83, 'Precision_score': 0.89, 'Fbeta_score': 0.84})

class XceptionModel(APIView):
    
    def get(self, request):
        return Response({'Recall_score': 0.68, 'Precision_score': 0.82, 'Fbeta_score': 0.68})
    
class GetBestPrediction(APIView):    
    
    def get(self, request):
        cnn_model = CNN_Prediction()
        tensors = cnn_model.process_images()
        selected_model = cnn_model.build_ResNet50_Deep()
        predictions = cnn_model.predict_image(selected_model, tensors)
        labels = cnn_model.convert_prediction(predictions)
        return Response({'predictions': labels})


class GetImagePrediction(APIView):
    
    def post(self, request):    
        print(request.data)
        filelink = request.data['imageName']
        filename = request.data['image']
        selection = request.data['modelName']
        handle_uploaded_file(request.FILES['image'], filelink)
        
        cnn_model = CNN_Prediction()
        tensors = cnn_model.process_image(filelink)
        
        if selection == 'ResNet50_deep':
            selected_model = cnn_model.build_ResNet50_Deep()
        elif selection == 'ResNet50_shallow':
            selected_model = cnn_model.build_ResNet50_Shallow()
        elif selection == 'Xception':
            selected_model = cnn_model.build_Xception()
        elif selection == 'original':
            selected_model = cnn_model.build_Original()
            
        predictions = cnn_model.predict_image(selected_model, tensors)
        labels = cnn_model.convert_prediction(predictions)
        cnn_model.clear_models()
        
        print('finish prediction')
        return Response({'Location': 'images/' + filelink, 'prediction': labels})


'''
class GetImageUploadPredictionViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    
    queryset = ImageUpload.objects.all()
    serializer_class = ImageUploadSerializer
    
    def __init__(self, *args, **kwargs):
        super(GenericViewSet, self).__init__(*args, **kwargs)
    
    @list_route(methods=['post'])
    @parser_classes((FormParser, MultiPartParser,))
    def image(self, request, *args, **kwargs):
        print('request')
        print(request.data)
        if 'image' in request.data:
            upload = request.data['image']
            user_image = ImageUpload()
            user_image.save(upload)
            return Response(status=HTTP_201_CREATED, headers={'Location': user_image.image.url})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
            

pickle_model_history = []
with (open('saved_models/original_model', "rb")) as openfile:
    while True:
        try:
            pickle_model_history.append(pickle.load(openfile))
        except EOFError:
            break

print(pickle_model_history)
'''
        

        
