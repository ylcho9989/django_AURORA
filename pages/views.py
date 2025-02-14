from django.shortcuts import render

def mainpage(request):
    # 로그인 여부에 따라 다른 메시지 전달
    if request.user.is_authenticated:
        message = "로그인을 했습니다."
    else:
        message = "로그아웃을 했습니다. 메인화면입니다."

    return render(request, 'pages/mainpage.html', {'message': message})
