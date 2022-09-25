from django import template

from newsletters.forms import JoinForm
# from newsletters.views import get_success_message

register = template.Library()


@register.inclusion_tag('newsletters/join_form.html')
def join():
    return {"join": JoinForm()}


# @register.inclusion_tag('newsletters/allert_message.html')
# def allert_message():
#     return {"allert_message": get_success_message}
