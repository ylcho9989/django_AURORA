from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import WebLink
from .forms import WebLinkForm

@login_required
def add_link(request):
    if request.method == "POST":
        form = WebLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.created_by = request.user  # 현재 로그인한 사용자를 생성자로 저장
            link.save()
            return redirect('mainpage')  # 저장 후 메인 페이지로 이동
    else:
        form = WebLinkForm()
    return render(request, 'links/add_link.html', {'form': form})
@login_required
def list_links(request):
    links = WebLink.objects.filter(created_by=request.user)  # ✅ 현재 로그인한 사용자가 등록한 웹 링크만 가져오기
    return render(request, 'links/list_links.html', {'links': links})

