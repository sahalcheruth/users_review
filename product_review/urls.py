# product_review/urls.py
from django.contrib import admin
from django.urls import path, include
from reviews.views import home_view ,login_view ,register_view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', include('reviews.urls')),
    path('home',home_view,name='home')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
