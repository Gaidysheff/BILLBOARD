from django.urls import path

from .views import (
    about, PostsHome,
    # ShowPost,
    FeedbackList,
    # show_category,
    PostsInCategory,
    #  add_comment_to_post, feedback_to_post,
    AddBlog, UpdateBlog, DeleteBlog, contact, LoginUser,
    show_post,
    # UserPosts,
    post_comments_user,
)
from customuser.views import signup

urlpatterns = [
    path('', PostsHome.as_view(), name='home'),
    # path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('post/<slug:post_slug>/', show_post, name='post'),

    # path('<slug:post_slug>/', feedback_to_post, name='new_feedback'),

    path('feedback/', FeedbackList.as_view(), name='feedback'),
    path('category/<slug:cat_slug>/', PostsInCategory.as_view(), name='category'),
    path('about/', about, name='about'),
    path('addblog/', AddBlog.as_view(), name='add_blog'),
    path('post/<slug:post_slug>/update/',
         UpdateBlog.as_view(), name='update_blog'),
    path('post/<slug:post_slug>/delete/',
         DeleteBlog.as_view(), name='delete_blog'),
    # path('post/<slug:post_slug>/comment/', add_comment_to_post, name='comment'),

    path('userposts/', post_comments_user, name='userposts'),

    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('signup/', signup, name='signup')
]
