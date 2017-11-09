from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from .views import (CustomerRegistrationView, CustomerEmailVerificationView,UserProfileDashboard, CreateClerkView,
                    ClerkListView, ban_clerk_account, restore_clerk_account)

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    url(r'^register/$', CustomerRegistrationView.as_view(), name='register'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^verify/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        CustomerEmailVerificationView.as_view(), name='verify_email'),
    url(r'^dashboard/$', login_required(UserProfileDashboard.as_view()), name='profile_dashboard'),
    url(r'^clerk/create/$', login_required(CreateClerkView.as_view()), name='create_clerk'),
    url(r'^clerk/list/$', login_required(ClerkListView.as_view()), name='clerk_list'),
    url(r'^clerk/block/(?P<user_pk>[0-9]+)/$', login_required(ban_clerk_account), name='clerk_ban'),
    url(r'^clerk/restore/(?P<user_pk>[0-9]+)/$', login_required(restore_clerk_account), name='clerk_restore')

]
