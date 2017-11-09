from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import CreateOrderView, OrderList, DetailOrderView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', login_required(DetailOrderView.as_view()), name='detail'),
    url(r'^create/$', login_required(CreateOrderView.as_view()), name='create'),
    url(r'^list/$', OrderList.as_view(), name='list'),
    url(r'^list/(?P<status>[0-9]+)$', OrderList.as_view(), name='list'),

]
