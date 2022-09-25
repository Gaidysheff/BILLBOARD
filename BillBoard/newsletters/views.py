from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import JoinForm
from .models import Join


class JoinView(SuccessMessageMixin, CreateView):
    model = Join
    form_class = JoinForm
    success_url = reverse_lazy('home')

    def get_success_message(self, cleaned_data):
        return 'Thank you for joining'

# # функция для (FormView)
#     def from_valid(self, form):
#         email = form.cleaned_data.get('email')
#         return super(JoinView, self).form_valid(form)
