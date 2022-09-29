from django.contrib.messages.views import SuccessMessageMixin
from newsletters.models import Join
from newsletters.forms import JoinForm
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.handlers import exception
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView,
    UpdateView,
)

from .forms import AddPostForm, CommentForm
from .models import Category, Post, Feedback
from .utilities import DataMixin, menu


class PostsHome(DataMixin, ListView):
    model = Post
    template_name = 'blogging/HomePage.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Post.objects.all()

# __________________________________________


class JoinView(SuccessMessageMixin, CreateView):
    model = Join
    form_class = JoinForm
    success_url = reverse_lazy('home')

    def get_success_message(self, cleaned_data):
        return 'Thank you for joining'

# __________________________________________


# class ShowPost(DataMixin, DetailView):
#     model = Post
#     template_name = 'blogging/post.html'
#     slug_url_kwarg = 'post_slug'
#     context_object_name = 'post'

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title=context['post'])
#         return dict(list(context.items()) + list(c_def.items()))

# _________________________________________________________________
def show_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    feedbacks = post.feedbacks.filter(status=True)
    new_feedback = None
    # Comment posted
    if request.method == 'POST':
        feedback_form = CommentForm(data=request.POST)
        if feedback_form.is_valid():
            # Create Comment object but don't save to database yet
            new_feedback = feedback_form.save(commit=False)
            # Assign the current post to the comment
            new_feedback.post = post
            # Save the comment to the database
            new_feedback.save()
    else:
        feedback_form = CommentForm()

    context = {
        'menu': menu,
        'post': post,
        'title': post.title,
        'cat_selected': post.cat_id,
        'feedbacks': feedbacks,
        'new_feedback': new_feedback,
        'feedback_form': feedback_form,
    }

    return render(request, 'blogging/post.html', context=context)
# _________________________________________________________________


class PostsInCategory(DataMixin, ListView):
    model = Post
    template_name = 'blogging/HomePage.html'
    context_object_name = 'posts'
    # allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'blogging/login.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Авторизация")
    #     return dict(list(context.items()) + list(c_def.items()))


class AddBlog(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blogging/addblog.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class UpdateBlog(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = AddPostForm
    model = Post
    template_name = 'blogging/updateblog.html'
    # success_url = reverse_lazy('home')
    # login_url = reverse_lazy('home')
    # raise_exception = True


class DeleteBlog(LoginRequiredMixin, DataMixin, DeleteView):
    model = Post
    template_name = 'blogging/deleteblog.html'
    success_url = reverse_lazy('home')


# def add_comment_to_post(request, post_slug):
#     if request.method == "POST":
#         user = request.user
#         post = get_object_or_404(Post, slug=post_slug)
#         form = CommentForm(request.POST, instance=post)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = user
#             comment.post = post
#             comment.save()
#             form.save()
#             return redirect('blogging:post_detail')  # post.id
#     else:
#         form = CommentForm()
#     return render(request, 'blogging/add_comment_to_post.html', {'form': form})

# ---------------------------------------------------------------------------


# def feedback_to_post(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#     feedbacks = post.feedbacks.filter(status=True)
#     new_feedback = None
#     # Comment posted
#     if request.method == 'POST':
#         feedback_form = CommentForm(data=request.POST)
#         if feedback_form.is_valid():

#             # Create Comment object but don't save to database yet
#             new_feedback = feedback_form.save(commit=False)
#             # Assign the current post to the comment
#             new_feedback.post = post
#             # Save the comment to the database
#             new_feedback.save()
#     else:
#         feedback_form = CommentForm()
#     return render(request, 'blogging/post.html', {'post': post, 'feedbacks': feedbacks, 'new_feedback': new_feedback, 'feedback_form': feedback_form})


# ---------------------------------------------------------------------------

class FeedbackList(DataMixin, ListView):
    model = Feedback
    template_name = 'blogging/feedback_list.html'
    context_object_name = 'feedback_list'

    def get_queryset(self):
        return Feedback.objects.all()


def about(request):
    return render(request, 'blogging/about.html', {'title': 'О сайте'})


def contact(request):
    return HttpResponse("<h1>Контакты</h1>")


def pageNotFound(request, exception):
    return render(request, 'blogging/PageNotFound.html')
