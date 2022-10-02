from multiprocessing import context

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, ListView,
                                  UpdateView)
from newsletters.forms import JoinForm
from newsletters.models import Join

from .forms import AddPostForm, CommentForm
from .models import Category, Feedback, Post
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


class JoinView(SuccessMessageMixin, CreateView):
    model = Join
    form_class = JoinForm
    success_url = reverse_lazy('home')

    def get_success_message(self, cleaned_data):
        return 'Thank you for joining'


def show_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    feedbacks = post.feedbacks.filter(status=True)
    new_feedback = None

    if request.method == 'POST':
        feedback_form = CommentForm(data=request.POST)
        if feedback_form.is_valid():
            new_feedback = feedback_form.save(commit=False)
            new_feedback.post = post
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
    post_author = post.author.email
    _a = Feedback.objects.all()
    _au = _a[len(_a)-1]
    feedback_author = _au.author

    send_mail(
        subject=f'Feedbak for { post } received',
        message=f'Получен отклик на Ваш пост "{ post }" от { feedback_author }',
        from_email='gaidysheff@yandex.ru',
        recipient_list=['gaidysheff@mail.ru', str(post_author)]
    )

    return render(request, 'blogging/post.html', context=context)


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


class AddBlog(LoginRequiredMixin, DataMixin, CreateView):
    model = Post
    form_class = AddPostForm
    template_name = 'blogging/addblog.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить пост")
        return dict(list(context.items()) + list(c_def.items()))


class UpdateBlog(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = AddPostForm
    model = Post
    template_name = 'blogging/updateblog.html'


class DeleteBlog(LoginRequiredMixin, DataMixin, DeleteView):
    model = Post
    template_name = 'blogging/deleteblog.html'
    success_url = reverse_lazy('home')


def post_comments_user(request, user):
    # userpost = Post.objects.filter(author=user)
    # num_comments = Feedback.objects.filter(post=userpost)

    # context = {
    #     'userpost': userpost,
    #     'num_comments': num_comments,
    # }
    pass
    return render(request, 'blogging/user_post_list.html', context)


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


# from .utils.permissions import IsAuthorMixin, NotIsAuthorMixin
# IsAuthorMixin
class FeedbacksList(View):
    def get(self, request, *args, **kwargs):
        post_slug = self.kwargs['post_slug']
        post = Post.objects.get(slug=post_slug)
        queryset = Feedback.objects.order_by('-dateCreation').filter(post=post)

        context = {
            'feedbacks': queryset,
            'post': post
        }

        return render(request, 'blogging/feedbacks_list.html', context)
