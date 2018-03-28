from django.conf.urls import url
from sale import views

urlpatterns = [
    url(r'^$', views.dashboard, name="sales_dashboard"),
]
