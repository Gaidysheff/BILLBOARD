from django.urls import path

from .views import (
    about, PostsHome,
    ShowPost,
    show_category,
    # PostsCategory,
    AddBlog, UpdateBlog, DeleteBlog, contact, LoginUser,
    #  show_post,
)
from customuser.views import SignUp

urlpatterns = [
    path('', PostsHome.as_view(), name='home'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    # path('post/<slug:post_slug>/', show_post, name='post'),
    # path('cat/<slug:category_slug>', PostsCategory.as_view(), name='category'),
    path('cat/<int:cat_id>', show_category, name='category'),
    path('about/', about, name='about'),
    path('addblog/', AddBlog.as_view(), name='add_blog'),
    path('post/<slug:post_slug>/update/', UpdateBlog.as_view(), name='update_blog'),
    # path('post/<int:cat_id>/update/', UpdateBlog.as_view(), name='update_blog'),
    path('post/<slug:post_slug>/delete/', DeleteBlog.as_view(), name='delete_blog'),
    # path('post/<int:cat_id>/delete/', DeleteBlog.as_view(), name='delete_blog'),

    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup')
]
