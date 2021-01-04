from django.urls import path
from django.http import HttpResponse
from django.conf.urls import url
from .  import views

# Create your tests here.
'''
urlpatterns = [
    path('rai', views.rai, name='rai'),
    path('', views.youtube, name='youtube'),
    path('', views.index, name='index'),
   
]
'''

urlpatterns = [
    path('', lambda request: HttpResponse('Is the upload index page')),
    path('youtube/', views.uploadyoutube, name='uyoutube'),
    path('rai/', views.uploadrai, name='urai'),

]