from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WebLink, SharedWebLink
from .forms import WebLinkForm
from django.contrib.auth.models import User
from django.contrib import messages

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
    query = request.GET.get('query', '')  # 검색어 가져오기 (없으면 빈 문자열)
    category = request.GET.get('category', '')  # 선택된 카테고리 가져오기

    # 기본적으로 현재 사용자가 생성한 링크 가져오기
    links = WebLink.objects.filter(created_by=request.user)

    # 공유된 링크 추가 (공유된 모든 링크 포함)
    shared_links = WebLink.objects.filter(shared_users__shared_with=request.user)

    # 편집 권한(쓰기 권한)이 있는 공유된 웹 링크
    shared_editable_links = WebLink.objects.filter(
        shared_users__shared_with=request.user, shared_users__can_edit=True)

    # 필터 적용 (검색어 및 카테고리)
    if query:
        links = links.filter(name__icontains=query)  # 제목에 검색어가 포함된 경우
        shared_links = shared_links.filter(name__icontains=query)

    if category:
        links = links.filter(category=category)
        shared_links = shared_links.filter(category=category)

    return render(
        request,
        'links/list_links.html',
        {
            'links': links | shared_links,  # 검색 및 필터링된 링크 전달
            'shared_editable_links': shared_editable_links,  # 편집 가능한 링크 전달
            'query': query,  # 템플릿에서 검색어 유지
            'category': category,  # 템플릿에서 카테고리 유지
        },
    )

@login_required
def edit_link(request, link_id):
    link = get_object_or_404(WebLink, id=link_id)

    # 사용자가 직접 생성했거나, 공유된 링크이고 편집 권한이 있는 경우만 허용
    if link.created_by != request.user:
        shared_link = SharedWebLink.objects.filter(web_link=link, shared_with=request.user, can_edit=True).first()
        if not shared_link:
            messages.error(request, "이 링크를 수정할 권한이 없습니다.")
            return redirect('list_links')

    if request.method == "POST":
        form = WebLinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            messages.success(request, "링크가 수정되었습니다.")
            return redirect('list_links')
    else:
        form = WebLinkForm(instance=link)

    return render(request, 'links/edit_link.html', {'form': form})


@login_required
def delete_link(request, link_id):
    link = get_object_or_404(WebLink, id=link_id)

    # 삭제 권한 확인 (생성자이거나, 공유된 링크에서 `can_edit=True`인 경우)
    if link.created_by != request.user:
        shared_link = SharedWebLink.objects.filter(web_link=link, shared_with=request.user, can_edit=True).first()
        if not shared_link:
            messages.error(request, "이 링크를 삭제할 권한이 없습니다.")
            return redirect('list_links')

    link.delete()
    messages.success(request, "링크가 삭제되었습니다.")
    return redirect('list_links')


@login_required
def share_link(request, link_id):
    link = get_object_or_404(WebLink, id=link_id)

    if request.method == "POST":
        username = request.POST.get('username')
        can_edit = request.POST.get('can_edit') == 'on'

        try:
            shared_user = User.objects.get(username=username)

            # 이미 공유된 사용자라면 중복 추가하지 않음
            if SharedWebLink.objects.filter(web_link=link, shared_with=shared_user).exists():
                messages.warning(request, f"{username}님에게 이미 공유된 링크입니다.")
            else:
                SharedWebLink.objects.create(web_link=link, shared_with=shared_user, can_edit=can_edit)
                messages.success(request, f"{username}님과 링크가 공유되었습니다.")

        except User.DoesNotExist:
            messages.error(request, "해당 사용자 이름이 존재하지 않습니다.")

        return redirect('list_links')

    return render(request, 'links/share_link.html', {'link': link})

@login_required
def search_links(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')

    links = WebLink.objects.filter(created_by=request.user)

    if query:
        links = links.filter(name__icontains=query)  # 부분 일치 검색

    if category:
        links = links.filter(category=category)

    return render(request, 'links/list_links.html', {'links': links, 'query': query, 'category': category})
