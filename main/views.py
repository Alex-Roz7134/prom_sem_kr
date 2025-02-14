import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from main.forms import LoginForm, AddSnippetForm
from main.models import Snippet


def get_base_context(request, pagename):
    return {
        'pagename': pagename,
        'loginform': LoginForm(),
        'user': request.user,
    }


def index_page(request):
    context = get_base_context(request, 'PythonBin')
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = get_base_context(request, 'Добавление нового сниппета')
    if request.method == 'POST':
        addform = AddSnippetForm(request.POST)
        if addform.is_valid():
            record = Snippet(
                name=addform.cleaned_data['name'],
                code=addform.cleaned_data['code'],
                creation_date=datetime.datetime.now(),
                user=request.user if request.user.is_authenticated else None,  # Сохраняем пользователя, если он авторизован
            )
            record.save()
            id = record.id
            messages.add_message(request, messages.SUCCESS, "Сниппет успешно добавлен")
            return redirect('view_snippet', id=id)
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме")
            return redirect('add_snippet')
    else:
        # Указываем текущего пользователя в поле `user`, если он авторизован
        context['addform'] = AddSnippetForm(
            initial={
                'user': request.user if request.user.is_authenticated else 'AnonymousUser',
            }
        )
    return render(request, 'pages/add_snippet.html', context)
def my_snippets_page(request):
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': Snippet.objects.filter(user=request.user),  # Фильтруем сниппеты по текущему пользователю
    }
    return render(request, 'pages/my_snippets.html', context)
def search_snippet_page(request):
    if request.method == 'POST':
        snippet_id = request.POST.get('snippet_id')
        if snippet_id and snippet_id.isdigit():
            try:
                snippet = Snippet.objects.get(id=int(snippet_id))
                return redirect('view_snippet', id=snippet.id)
            except Snippet.DoesNotExist:
                messages.add_message(request, messages.ERROR, f"Сниппет с ID {snippet_id} не найден.")
        else:
            messages.add_message(request, messages.ERROR, "Введите корректный ID.")
    return redirect('index')

def view_snippet_page(request, id):
    context = get_base_context(request, 'Просмотр сниппета')
    try:
        record = Snippet.objects.get(id=id)
        context['addform'] = AddSnippetForm(
            initial={
                'user': record.user.username if record.user else 'AnonymousUser',  # Показываем автора
                'name': record.name,
                'code': record.code,
            }
        )
    except Snippet.DoesNotExist:
        raise Http404
    return render(request, 'pages/view_snippet.html', context)


def login_page(request):
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = loginform.data['username']
            password = loginform.data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Авторизация успешна")
            else:
                messages.add_message(request, messages.ERROR, "Неправильный логин или пароль")
        else:
            messages.add_message(request, messages.ERROR, "Некорректные данные в форме авторизации")
    return redirect('index')


def logout_page(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Вы успешно вышли из аккаунта")
    return redirect('index')


def my_snippets_page(request):
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': Snippet.objects.filter(user=request.user),
    }
    return render(request, 'pages/my_snippets.html', context)
