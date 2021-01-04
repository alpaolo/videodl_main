from django.urls import path
from django.http import HttpResponse
from django.conf.urls import url
from .  import views

# Create your tests here.


urlpatterns = [
    path('', lambda request: HttpResponse('Is the download index page')),
    path('youtube/', views.downloadyoutube, name='dyoutube'),
    #path('youtube/?action=finished', views.finishdownloadyoutube, name='dfinishyoutube'),
    path(r'youtube/(?P<action>\w+)/$', views.downloadyoutube, name='dyoutube'),
    url('finish/', views.download_finish, name='dfinish'),
    url('rai/', views.downloadrai, name='drai'),

]