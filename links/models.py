from django.db import models
from django.contrib.auth.models import User

class WebLink(models.Model):
    CATEGORY_CHOICES = [
        ("personal", "개인 즐겨찾기"),
        ("work", "업무 활용 자료"),
        ("reference", "참고 자료"),
        ("education", "교육 및 학습 자료"),
    ]

    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links")  # 생성자
    name = models.CharField(max_length=255)  # 웹 링크 이름
    url = models.URLField()  # 웹사이트 URL
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # 카테고리
    shared_with = models.ManyToManyField(User, related_name="shared_links", blank=True)  # 공유된 사용자

    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 업데이트 시간

    def __str__(self):
        return self.name
