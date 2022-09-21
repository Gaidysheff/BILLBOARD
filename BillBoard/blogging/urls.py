from django.urls import path

from .views import (
    about, show_category, index, addblog, contact, LoginUser, show_post,
)
from customuser.views import SignUp

urlpatterns = [
    path('', index, name='home'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('cat/<int:cat_id>', show_category, name='category'),
    path('about/', about, name='about'),
    path('addblog/', addblog, name='add_blog'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup')
]
