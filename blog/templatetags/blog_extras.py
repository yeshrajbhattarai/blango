from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from blog.models import Post
import logging

register = template.Library()
User = get_user_model()

logger = logging.getLogger(__name__)

@register.filter
def author_details(author, current_user=None):
    if not isinstance(author, User):
        return ""

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = author.username

    if author.email:
        return format_html(
            '<a href="mailto:{}">{}</a>',
            author.email,
            name
        )

    return format_html("{}", name)


@register.inclusion_tag("blog/recent-posts.html")
def recent_posts(current_post, limit=5):
    posts = (
        Post.objects
        .exclude(pk=current_post.pk)
        .order_by("-published_at")[:limit]
    )
    logger.debug(
        "Loaded %d recent posts for post %d",
        len(posts),
        current_post.pk
    )
    return {"recent_posts": posts}


@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)

@register.simple_tag
def endrow():
    return format_html("</div>")

@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
    return format_html("</div>")