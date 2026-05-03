from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')


def set_theme(request):
    theme = request.GET.get('theme', 'light')
    if theme not in ('light', 'dark'):
        theme = 'light'
    next_url = request.GET.get('next', '/')
    response = redirect(next_url)
    response.set_cookie('sanad_theme', theme, max_age=60 * 60 * 24 * 365, samesite='Lax')
    return response