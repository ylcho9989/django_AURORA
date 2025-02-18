from django.urls import path
from .views import add_link, list_links, edit_link, delete_link, share_link, search_links

urlpatterns = [
    path('add/', add_link, name='add_link'),
    path('list/', list_links, name='list_links'),
    path('edit/<int:link_id>/', edit_link, name='edit_link'),  # 수정
    path('delete/<int:link_id>/', delete_link, name='delete_link'),  # 삭제
    path('share/<int:link_id>/', share_link, name='share_link'),  # 공유
    path('search/', search_links, name='search_links'),  # 검색
]
