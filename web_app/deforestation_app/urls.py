from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers

from deforestation_app import models

router = routers.DefaultRouter()
router.register(r'deforestation_app/api/predict', models.GetImageUploadPredictionViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^$', TemplateView.as_view(template_name='frontend/index.html')),
    url(r'^deforestation_app/api/original', models.OriginalModel.as_view()),
    url(r'^deforestation_app/api/resnet-shallow', models.ResNet50ModelShallow.as_view()),
    url(r'^deforestation_app/api/resnet-deep', models.ResNet50ModelDeep.as_view()),
    url(r'^deforestation_app/api/xception', models.XceptionModel.as_view()),
    url(r'^deforestation_app/api/predict-best', models.GetBestPrediction.as_view())
]
