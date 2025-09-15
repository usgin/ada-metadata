from django.urls import path
from .views import *



urlpatterns = (
#    path('', IndexPageView, name='index'),
    path('recorddoijsonld', recordJSONByDOIView, name='recordjsonld'),
    path('recorddoipds', pdsLabel, name='recordpds'),
)