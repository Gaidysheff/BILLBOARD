from django.urls import path
from .views import index, category

urlpatterns = [
    path('', index, name='home'),
    path('cat/<str:type>', category, name='category'),
]
