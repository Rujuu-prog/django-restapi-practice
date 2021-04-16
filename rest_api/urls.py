from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #api/というurlにアクセスがあった際は、api.urlsを参照するように設定
    path('api/', include('api.urls')),
]
