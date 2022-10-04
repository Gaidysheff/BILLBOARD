from blogging.utils.permissions import IsAuthorMixin, NotIsAuthorMixin
from multiprocessing import context

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
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
    feedbacks = post.feedbacks.filter(approved=True)
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


class UpdateBlog(IsAuthorMixin, UpdateView):
    form_class = AddPostForm
    model = Post
    template_name = 'blogging/updateblog.html'
    permission_required = ('post.add_blog',)
    success_url = reverse_lazy('home')

    def get_object(self, **kwargs):
        slug = self.kwargs.get('post_slug')
        return Post.objects.get(slug=slug)

    def get_context():
        context = {'title': "Обновление поста"}
        return context


class DeleteBlog(IsAuthorMixin, DeleteView):
    model = Post
    template_name = 'blogging/deleteblog.html'
    permission_required = ('post.post_delete',)
    success_url = reverse_lazy('home')

    def get_object(self, **kwargs):
        slug = self.kwargs.get('post_slug')
        return Post.objects.get(slug=slug)

    def get_context():
        context = {'title': "Удаление поста"}
        return context


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


class FeedbacksList(IsAuthorMixin, View):  # IsAuthorMixin,
    def get(self, request, *args, **kwargs):
        post_slug = self.kwargs['post_slug']
        post = Post.objects.get(slug=post_slug)
        queryset = Feedback.objects.order_by('-dateCreation').filter(post=post)

        context = {
            'feedbacks': queryset,
            'post': post
        }
        context['title'] = "Приватно для пользователя"

        return render(request, 'blogging/feedbacks_list.html', context)


class FeedbackAccept(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        feedback_pk = kwargs['feedback_pk']

        feedback = Feedback.objects.get(pk=feedback_pk)
        feedback.approved = True
        feedback.save()

        context = {
            'title': "Комментарий принят"
        }

        return render(request, 'blogging/feedback_accept.html', context)


class FeedbackReject(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        feedback_pk = kwargs['feedback_pk']

        feedback = Feedback.objects.get(pk=feedback_pk)
        feedback.approved = False
        feedback.save()

        return redirect(request.META['HTTP_REFERER'])


class FeedbackDelete(LoginRequiredMixin, DeleteView):
    model = Feedback
    template_name = 'blogging/feedback_delete.html'
    success_url = 'home'
    permission_required = ('blogging.feedback_delete')
    context_object_name = 'feedback'

    def get_object(self, **kwargs):
        feedback_id = self.kwargs.get('feedback_pk')
        feedback = Feedback.objects.get(pk=feedback_id)
        return feedback
