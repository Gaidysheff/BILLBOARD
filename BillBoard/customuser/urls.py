from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'), 
    # path('signup/', views.SignUp.as_view(), name='signup'), 
    ]
