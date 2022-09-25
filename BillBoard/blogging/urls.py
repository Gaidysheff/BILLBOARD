from django.urls import path

from .views import (
    about, PostsHome,
    ShowPost,
    # show_category,
    PostsInCategory,
    AddBlog, UpdateBlog, DeleteBlog, contact, LoginUser,
    #  show_post,
)
from customuser.views import signup

urlpatterns = [
    path('', PostsHome.as_view(), name='home'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', PostsInCategory.as_view(), name='category'),
    path('about/', about, name='about'),
    path('addblog/', AddBlog.as_view(), name='add_blog'),
    path('post/<slug:post_slug>/update/',
         UpdateBlog.as_view(), name='update_blog'),
    path('post/<slug:post_slug>/delete/',
         DeleteBlog.as_view(), name='delete_blog'),

    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('signup/', signup, name='signup')
]
