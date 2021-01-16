from django import template
import re

register = template.Library()


@register.filter
def make_paragraphs(text):
    paragraphs = re.split(r'[\r\n]+', text)
    result = ''
    for paragraph in paragraphs:
        result += f'<p class="single-card__section-text">{paragraph}</p>'
    return result
