from django import template
from blog.models import ReplyComment
from base.views import printer

register = template.Library()


@register.filter
def evaler(lst):
    return eval(lst)


@register.filter
def reply(comment):
    replies = ReplyComment.objects.filter(comment=comment)
    replies = list(replies)
    replies.reverse()
    return replies
