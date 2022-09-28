from django import template
from blogging.models import Category, Feedback, Post


register = template.Library()


@register.inclusion_tag('blogging/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, 'cat_selected': cat_selected}


@register.simple_tag()
def get_feedback():
    return Post.objects.get(id=2).feedback_set.all()
