from django.contrib import admin
from django.urls import path, include
from .views import mainpage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', mainpage, name='mainpage'),  # 메인 페이지 연결
]