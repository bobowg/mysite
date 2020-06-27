from django.urls import path
from . import views

urlpatterns = [
  path('update_likechange/',views.update_likechange,name='update_likechange'),
]