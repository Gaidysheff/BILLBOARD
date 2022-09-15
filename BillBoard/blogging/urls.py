from django.urls import path

from .views import about, category, index

urlpatterns = [
    path('', index, name='home'),
    path('cat/<str:type>', category, name='category'),
    path('about/', about, name='about'),
]
