from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from django.urls import path, include
from . import views
from .views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, AddressView, LogoutView

urlpatterns = [
    # path('register/', views.register, name="register"),  # 注册
    # path('register_handle/', views.register_handle, name="register_handle")  # 注册处理
    path('register/', RegisterView.as_view(), name='register'),  # 注册
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 用户激活
    url(r'^login$', LoginView.as_view(), name='login'),  # 登录ter
    url(r'^logout$', LogoutView.as_view(), name='logout'),  # 注销登录

    # url(r'^$', login_required(UserInfoView.as_view()), name='user'), # 用户中心-信息页
    # url(r'^order$', login_required(UserOrderView.as_view()), name='order'), # 用户中心-订单页
    # url(r'^address$', login_required(AddressView.as_view()), name='address'), # 用户中心-地址页

    url(r'^$', UserInfoView.as_view(), name='user'),  # 用户中心-信息页
    url(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'), # 用户中心-订单页
    url(r'^address$', AddressView.as_view(), name='address'),  # 用户中心-地址页
]
