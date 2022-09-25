from django.urls import path
from newsletters.views import JoinView

urlpatterns = [
    path('join', JoinView.as_view(), name="join"),
]
