from django.shortcuts import render ,get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
from django.conf import settings
from django.core.cache import cache
from .models import BlogType,Blog
from read_statistics.utils import read_statistics_once_read,get_seven_days_read_data,get_today_hot_datas,get_yesterday_hot_datas,get_days_hot_datas
from blog.dj_from import LoginForm
# Create your views here.

def get_blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOG_NUMBER)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取前后各两页的范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    blog_dates = Blog.objects.dates('created_time', 'month', 'DESC')
    blog_date_disct ={}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_date_disct[blog_date] = blog_count
    context = {}
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count = Count('blog'))
    context['blog_dates'] = blog_date_disct
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_all_list)
    return render(request,'blog_list.html',context)

def blog_detail(request,blog_id):
    blog = get_object_or_404(Blog, id = blog_id)
    cookies = read_statistics_once_read(request,blog)
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt = blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt = blog.created_time).first()
    context['blog'] = blog
    context['login_from'] = LoginForm()
    response = render(request, 'blog_detail.html', context)
    response.set_cookie(cookies,'true')
    return response

def blog_with_type(request,type_id):
    blog_type = get_object_or_404(BlogType,pk=type_id)
    blogs_all_list =  Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context)
def blogs_with_days(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context["blog_datetime"] = '%s年%s月'% (year,month)
    return render(request,'blogs_with_days.html',context)

def home(request):
    contenttype = ContentType.objects.get_for_model(Blog)
    read_nums ,dates = get_seven_days_read_data(contenttype)
    #获取缓存数据
    weekday_hot_datas = cache.get('weekday_hot_datas')
    month_hot_datas = cache.get('month_hot_datas')
    if month_hot_datas is None:
        month_hot_datas = get_days_hot_datas(30)
        cache.set('month_hot_datas',month_hot_datas,3600)
    if weekday_hot_datas is None:
        weekday_hot_datas = get_days_hot_datas(7)
        cache.set('weekday_hot_datas',weekday_hot_datas,3600)
    context ={}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['hot_datas'] = get_today_hot_datas(contenttype)
    context['ys_hot_datas'] = get_yesterday_hot_datas(contenttype)
    context['weekday_hot_datas'] = weekday_hot_datas
    context['month_hot_datas'] = month_hot_datas
    return render(request,'home.html',context)

