from django.shortcuts import render
from .models import Submit, User, Comment, Usuari, Like
from django.views import generic
from .forms import HomeForm, CommentForm, AboutForm
from django.shortcuts import redirect, get_object_or_404

import sys

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def index(request):
    path = request.GET.get('path')
    if path:
        lista = list(Submit.objects.filter(path__exact=path).order_by('-likes'))
    else:
        lista = list(Submit.objects.filter(text__exact='').order_by('-likes'))
    return render(
        request,
        'index.html',
        context={'lista': lista},
    )


def userpage(request,pk):
    useract = Usuari.objects.get(user=pk)
    form = AboutForm()
    if request.method == "POST":
        form = AboutForm(request.POST,instance = useract)
        if form.is_valid():
            useract = form.save(commit=False)
            useract.save()

    return render(
        request,
        'hn/userpage.html',
        context = {'useract' : useract , 'form' : form}
    )

def sub_user(request,pk):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    useract = Usuari.objects.get(user=pk)
    listasub = list(Submit.objects.filter(author__exact = useract.user))

    return render(
        request,
        'hn/sub_user.html',
        context={'listasub':listasub},
    )

def com_user(request,pk):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    listacom = list(Comment.objects.filter(author__exact = request.user))

    return render(
        request,
        'hn/com_user.html',
        context={'listacom':listacom},
    )

def lik_user(request,pk):

    listalikes = list(Like.objects.filter(user__exact = request.user))
    print(listalikes, file=sys.stderr)
    listasub = list()
    for like in listalikes:
        id = like.post.id
        listasub.append(Submit.objects.get(pk=id))

    return render(
        request,
        'hn/lik_user.html',
        context={'listasub':listasub},
    )


def new(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    listaordenada = list(Submit.objects.all().order_by('-date_added'))

    return render(
        request,
        'hn/new.html',
        context={'listaordenada':listaordenada},
    )

def ask(request):
        # Genera contadores de algunos de los objetos principales
        listaask = list(Submit.objects.filter(url__exact=''))
        return render(
            request,
            'hn/ask.html',
            context={'listaask':listaask},
        )

def ask_ind(request,pk):
        # Genera contadores de algunos de los objetos principales
        form = CommentForm()
        submit_id = Submit.objects.get(pk=pk)
        listacomments = Comment.objects.filter(submit__exact = submit_id)
        comments_count = listacomments.count()
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.submit = submit_id
                comment.author = User.objects.get(id=request.user.id)
                comment.save()
        return render(request,'hn/ask_ind.html',{'submit' : submit_id, 'form': form, 'listacomments': listacomments})


def submit(request):
    # Creamos un formulario vacío
        form = HomeForm()
    # Comprobamos si se ha enviado el formulario
        if request.method == "POST":
        # Añadimos los datos recibidos al formulario
            form = HomeForm(request.POST)
        # Si el formulario es válido...
            if form.is_valid():
                if form.cleaned_data['url']:
                    if not form.cleaned_data['text']:
                        num_results = Submit.objects.filter(url = form.cleaned_data['url']).count()
                        if num_results > 0:
                            return redirect('/')
                        else:
                            submit = form.save(commit=False)
                            submit.path = dividir(submit.url)
                            print(request.user, file=sys.stderr)
                            submit.author = User.objects.get(id=request.user.id)
                            submit.save()
                            return redirect('/')
                if not form.cleaned_data['url']:
                    if form.cleaned_data['text']:
                        submit = form.save(commit=False)
                        submit.author = User.objects.get(id=request.user.id)
                        submit.save()
                        return redirect('/')
                else:
                        return redirect('/') #mostrar que no se ha podido enviar
    # Si llegamos al final renderizamos el formulario
        return render(request, "hn/submit.html", {'form': form})








def dividir(CharField):
    path = CharField.split('/')
    aux = CharField

    if len(path) > 1:
        if path[0] == 'https:' or path[0] == 'http:':
            aux = path[2]
        else:
            aux = path[0]
    else:
        aux = path[0]
    res = aux.split('.')
    if res[0] == 'www':
        res.remove('www')
    resultado = ''
    primero=True
    for p in res:
        if primero:
            resultado += p
            primero=False
        else:
            resultado = resultado + '.' + p
    return (resultado)


def like(request):
    red = request.GET.get('path')
    if request.method == "GET":
        pk = request.GET.get('pk')
        submit = Submit.objects.get(id=pk)
        submit.likes = submit.likes + 1
        submit.save()
#        print(submit.likes, file=sys.stderr)
    return redirect (red)

def like2(request):
    red = request.GET.get('path')
    if request.method == "GET":
        pk = request.GET.get('pk')
        post = get_object_or_404(Submit, id = pk)
        obj = ""
        valueobj = ""
        try:
            obj = Like.objects.get(user = request.user, post = post)
        except Like.DoesNotExist:
            ulike= Like()
            ulike.user = request.user
            ulike.post = post
            ulike.value = 5
            ulike.save()
            post.likes = post.likes + 1
            post.save()
    return redirect (red)


def dislike(request):
    red = request.GET.get('path')
    if request.method == "GET":
        pk = request.GET.get('pk')
        post = get_object_or_404(Submit, id = pk)
        obj = ""
        valueobj = ""
        try:
            obj = Like.objects.get(user = request.user, post = post)
            post.likes = post.likes - 1
            post.save()
            obj.delete()
        except Like.DoesNotExist:
            redirect(red)
    return redirect (red)
