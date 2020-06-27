import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.utils import timezone
from blog.models import Blog
from .models import ReadNum,ReadDetail
def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model,obj.id)
    if not request.COOKIES.get(key):
        #总阅读数
        read_num,created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.id)
        read_num.read_num +=1
        read_num.save()
        #当天阅读数
        dates = timezone.now().date()
        readDetail ,created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.id,date=dates)
        readDetail.read_num += 1
        readDetail.save()
    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7,0,-1):
        date =  today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_detail = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = read_detail.aggregate(read_num=Sum('read_num'))
        read_nums.append( result['read_num'] or 0)

    return read_nums ,dates

def get_today_hot_datas(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')
    return read_details[:5]
def get_yesterday_hot_datas(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:5]

def get_days_hot_datas(days):
    today = timezone.now().date()
    date = today - datetime.timedelta(days=days)
    read_details = Blog.objects.filter(read_details__date__lt =today, read_details__date__gte=date).values('id','title').annotate(read_nums =Sum('read_details')).order_by('-read_nums')
    return read_details[:5]