from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm
from likes.models import LikeCount,LikeRecoord
register = template.Library()
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    count = Comment.objects.filter(content_type=content_type,object_id=obj.id).count()
    return count
@register.simple_tag
def get_comment_from(obj):
    content_type = ContentType.objects.get_for_model(obj)
    commentform =  CommentForm(initial={'content_type': content_type.model, 'object_id': obj.id, 'reply_comment_id': 0})
    return commentform
@register.simple_tag
def get_comments(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.id, parent=None).order_by(
        '-comment_time')
    return comments
@register.simple_tag
def get_likecount(obj):
    content_type = ContentType.objects.get_for_model(obj)
    likecount , created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.id)
    return likecount.like_num
@register.simple_tag(takes_context=True)
def get_like_stauts(context,obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecoord.objects.filter(content_type = content_type,object_id = obj.id,user = user).exists():
        return 'active'
    else:
        return ''
@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model