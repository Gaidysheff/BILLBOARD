from blogging.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class IsAuthorMixin(LoginRequiredMixin):

    def get_slug_list(self, dict_):
        slugs = []
        for slug in dict_:
            slugs.append(slug.get('slug'))
        return slugs

    def get_pk_list(self, dict_):
        pks = []
        for pk in dict_:
            pks.append(pk.get('pk'))
        return pks

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        post_slug = kwargs.get('post_slug')
        feedback_pk = kwargs.get('feedback_pk')

        if post_slug:
            slugs_dict = request.user.posts.all().values('slug')
            if post_slug not in self.get_slug_list(slugs_dict):
                return self.handle_no_permission()

            return super().dispatch(request, *args, **kwargs)

        elif feedback_pk:
            pks_dict = request.user.feedback_set.all().values('pk')

            if feedback_pk not in self.get_pk_list(pks_dict):
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)

        return self.handle_no_permission()


class NotIsAuthorMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        post = Post.objects.filter(slug=kwargs.get('post_slug')).first()

        if post:
            if post in request.user.posts.all():
                return redirect('post')
        return super().dispatch(request, *args, **kwargs)
