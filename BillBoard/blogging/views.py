from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.handlers import exception
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm
from .models import Category, Post
from .utilities import DataMixin


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


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'blogging/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = context['post']
        return context


# _________________________________________________________________
# def show_post(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)

#     context = {
#         'menu': menu,
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.category_id,
#     }
#     return render(request, 'blogging/post.html', context=context)

# _________________________________________________________________


# class PostsCategory(ListView):
#     model = Post
#     template_name = 'newsapp/cat_index.html'
#     context_object_name = 'posts'
#     allow_empty = False

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Категория - ' + str(
#             context['posts'][0].category), cat_selected=context['posts'][0].category_id)
#         return dict(list(context.items()) + list(c_def.items()))

#     def get_queryset(self):
#         return Post.objects.filter(category__slug=self.kwargs['category_slug'])


# _________________________________________________________________
menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить блог", 'url_name': 'add_blog'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]


def show_category(request, cat_id):
    posts = Post.objects.filter(category=cat_id)

    if len(posts) == 0:
        return pageNotFound(request, exception)

    context = {
        'menu': menu,
        'posts': posts,
        'cat_selected': cat_id,
    }
    return render(request, 'blogging/HomePage.html', context=context)


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

def about(request):
    return render(request, 'blogging/about.html', {'title': 'О сайте'})


def contact(request):
    return HttpResponse("<h1>Контакты</h1>")


def pageNotFound(request, exception):
    return render(request, 'blogging/PageNotFound.html')
