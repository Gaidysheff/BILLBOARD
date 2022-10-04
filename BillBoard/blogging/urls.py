from django.urls import path

from .views import (about, PostsHome, FeedbackList, PostsInCategory, AddBlog, UpdateBlog,
                    DeleteBlog, contact, LoginUser, show_post, FeedbacksList,
                    FeedbackAccept, FeedbackReject, FeedbackDelete
                    )
from customuser.views import signup

urlpatterns = [
    path('', PostsHome.as_view(), name='home'),
    path('post/<slug:post_slug>/', show_post, name='post'),
    path('category/<slug:cat_slug>/', PostsInCategory.as_view(), name='category'),
    path('addblog/', AddBlog.as_view(), name='add_blog'),
    path('post/<slug:post_slug>/update/',
         UpdateBlog.as_view(), name='update_blog'),
    path('post/<slug:post_slug>/delete/',
         DeleteBlog.as_view(), name='delete_blog'),
    path('feedback/', FeedbackList.as_view(), name='feedback'),
    path('<slug:post_slug>/feedbacks/',
         FeedbacksList.as_view(), name='feedback_list'),

    path('<slug:post_slug>/feedbacks/<int:feedback_pk>/accept',
         FeedbackAccept.as_view(), name='feedback_accept'),
    path('<slug:post_slug>/feedbacks/<int:feedback_pk>/reject',
         FeedbackReject.as_view(), name='feedback_reject'),
    path('feedbacks/<int:feedback_pk>/delete',
         FeedbackDelete.as_view(), name='feedback_delete'),

    path('login/', LoginUser.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

]
