from django import template
from taggit.models import Tag

register = template.Library()


def revers_tags_list(tags, tag):
    tags.append(tag) if tag not in tags else tags.remove(tag)
    empty_item = ''
    while empty_item in tags:
        tags.remove('')
    return tags


@register.filter
def make_url(request, tag):
    if 'tags' in request.GET:
        source_tags = request.GET.get('tags').split(',')
    else:
        source_tags = [tag.name for tag in Tag.objects.all()]
    tags = revers_tags_list(source_tags, tag)
    return ','.join(tags)


# make from tags list url tags parameters string
@register.filter
def list_to_string(tags):
    return ','.join(tags)
