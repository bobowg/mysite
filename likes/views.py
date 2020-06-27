from django.shortcuts import render
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from .models import LikeCount,LikeRecoord
# Create your views here.
def ErrorResponse(code,message):
    data = {}
    data['stauts'] = 'Error'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)
def SuccessResponse(liked_num):
    data = {}
    data['stauts'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def update_likechange(request):
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(300, '你还没有登陆！')
    content_type = request.GET.get('content_type')
    object_id =int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        modle_class = content_type.model_class()
        modle_obj = modle_class.objects.get(pk =object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(302, '对象不存在！')

    if request.GET.get('is_like') == 'true':
       like_recoord,created = LikeRecoord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
       if created:
           like_count ,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
           like_count.like_num += 1
           like_count.save()
           return SuccessResponse(like_count.like_num)
       else:
           return ErrorResponse(303,'重复点赞！')
    else:
        if LikeRecoord.objects.filter(content_type=content_type,object_id=object_id,user=user).exists():
            like_record = LikeRecoord.objects.get(content_type=content_type,object_id=object_id,user=user)
            like_record.delete()
            like_count,created = LikeCount.objects.get_or_create(content_type=content_type,object_id=object_id)
            if not created:
                like_count.like_num -= 1
                like_count.save()
                return SuccessResponse(like_count.like_num)
            else:
                return ErrorResponse(404,'数据出错！')
        else:
            return ErrorResponse(403, '你没有点过赞！')
