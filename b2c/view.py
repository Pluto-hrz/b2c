from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def page_not_found(request):
    if not request.user:
        login = 0
    else:
        if request.user.character == 1:
            login = 1
        elif request.user.character == 0:
            login = 2
        else:
            login = 0
    return render(request, 'error404.html', locals())
