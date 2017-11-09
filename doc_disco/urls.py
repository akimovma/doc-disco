from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from users.views import Dashboard

urlpatterns = [
    url(r'^$', login_required(Dashboard.as_view()), name='dashboard'),
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
