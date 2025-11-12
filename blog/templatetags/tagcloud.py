from django import template
from ..models import Tag

register = template.Library()


@register.simple_tag
def tag_cloud(max_tags=30):
    tags = Tag.objects.all()[:max_tags]
    # compute simple weight based on number of posts
    tag_counts = []
    for t in tags:
        count = t.post_set.count()
        tag_counts.append((t, count))
    if not tag_counts:
        return []
    max_count = max(c for _, c in tag_counts) or 1
    weighted = []
    for t, c in tag_counts:
        weight = 1 + int((c / max_count) * 4)  # 1..5
        weighted.append({'tag': t, 'weight': weight})
    return weighted
