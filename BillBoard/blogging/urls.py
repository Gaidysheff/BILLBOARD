from django.urls import path

from .views import (
    about, category, index, addblog, contact, login,
)

urlpatterns = [
    path('', index, name='home'),
    path('cat/<str:type>', category, name='category'),
    path('about/', about, name='about'),
    path('addblog/', addblog, name='add_blog'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
]
