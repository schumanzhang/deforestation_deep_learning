from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers

from deforestation_app import models
from django.conf import settings
from django.conf.urls.static import static

#router = routers.DefaultRouter()
#router.register(r'upload', models.GetImageUploadPredictionViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^deforestation_app/api/original', models.OriginalModel.as_view()),
    url(r'^deforestation_app/api/resnet-shallow', models.ResNet50ModelShallow.as_view()),
    url(r'^deforestation_app/api/resnet-deep', models.ResNet50ModelDeep.as_view()),
    url(r'^deforestation_app/api/xception', models.XceptionModel.as_view()),
    url(r'^deforestation_app/api/predict-best', models.GetBestPrediction.as_view()),
    url(r'^deforestation_app/api/predict-image', models.GetImagePrediction.as_view())
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

