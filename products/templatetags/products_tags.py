from django import template
from base.views import printer
from products.models import ReplyReview

register = template.Library()


@register.filter
def evaler(lst):
    return eval(lst)


@register.filter
def reply(review):
    replies = ReplyReview.objects.filter(review=review)
    replies = list(replies)
    replies.reverse()
    return replies


@register.filter
def looper(limit):
    '''<option>2</option>'''
    options = ''
    for r in range(1, 1+limit):
        if r == 1:
            options += f'<option selected>{r}</option>'
        else:
            options += f'<option>{r}</option>'

    return options
