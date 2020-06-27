from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment
from django.contrib.contenttypes.models import ContentType
# Create your views here.
def update_comment(request):
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    data = {}
    coment_from =  CommentForm(request.POST,user=request.user)
    if coment_from.is_valid():
        comment = Comment()
        comment.user = coment_from.cleaned_data['user']
        comment.context = coment_from.cleaned_data['text'].strip()
        comment.content_object = coment_from.cleaned_data['content_object']
        parent = coment_from.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        data['status'] = 'Success'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.context
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data["reply_to"] = comment.reply_to.username
        else:
            data["reply_to"] = ""
        data["id"] = comment.id
        data["root_id"] = comment.root.id if not comment.root is None else ''
    else:
        data['status'] = 'Error'
    return JsonResponse(data)


