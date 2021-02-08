import re
from django import template
from taggit.models import Tag


register = template.Library()


def revers_tags_list(tags, tag):
    if tag not in tags:
        tags.append(tag)
    else:
        tags.remove(tag)
    tags = [tag for tag in tags if tag != '']
    return tags


@register.filter
def make_paragraphs(text):
    paragraphs = re.split(r'[\r\n]+', text)
    result = ''
    for paragraph in paragraphs:
        result += f'<p class="single-card__section-text">{paragraph}</p>'
    return result
 

@register.filter
def make_url(request, tag):
    if 'tags' in request.GET:
        source_tags = request.GET.get('tags').split(',')
    else:
        source_tags = [tag.name for tag in Tag.objects.all()]
    tags = revers_tags_list(source_tags, tag)
    return ','.join(tags)


@register.filter
def is_favorite(user, recipe):
    if user.favorites.filter(recipe=recipe).exists():
        return True
    return False


@register.filter
def recipes_word(num):
    if num in [11, 12, 13, 14]:
        return f'{num} рецептов'
    elif num % 10 == 1:
        return f'{num} рецепт'
    elif num % 10 in [2, 3, 4]:
        return f'{num} рецепта'
    else:
        return f'{num} рецептов'


@register.filter
def is_in_shopping_list(user, recipe):
    return user.recipes_to_shopping.filter(recipe=recipe).exists()


@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})
