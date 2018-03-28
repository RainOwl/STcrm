from django.conf.urls import url
from myadmin import views

urlpatterns = [
    url(r'^$', views.app_index),
    url(r'^login/', views.acc_login),
    url(r'^logout/', views.acc_logout, name="admin_logout"),
    url(r'^(\w+)/(\w+)/$', views.table_detail, name="table_detail"),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change, name="table_obj_change"),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete, name="table_obj_delete"),
    url(r'^(\w+)/(\w+)/add/$', views.table_obj_add, name="table_obj_add"),
]
