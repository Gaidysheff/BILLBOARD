from django_filters import FilterSet
from .models import Feedback


class FeedbackFilter(FilterSet):
    class Meta:
        model = Feedback
        fields = {
            'post': ['icontains', ],
            'approved': ['isnull', ],
            'dateCreation': ['date__lte', 'date__gt', ],
        }
