from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Item, Post
from .forms import ItemForm, PostForm
from django.contrib import messages





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)

            # Setea el password del usuario utilizando el método set_password
            user = User.objects.create_user(username=form.cleaned_data['user'].username)
            user.set_password(form.cleaned_data['password'])
            user.save()

            user_profile.user = user
            user_profile.save()

            return redirect('login')  # Redirige a la página de inicio de sesión después del registro
    else:
        form = RegistrationForm()

    return render(request, 'TuFeriaCL/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Autenticar al usuario
            user = authenticate(request, username=form.cleaned_data['user'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                # Redirigir a la página deseada después del inicio de sesión
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def index_views(request):
    return render(request, 'index.html') #redirige a la pagina principal

def about(request):
    return render(request, 'about.html') # redirige a la pagina about

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html') # Redirige al Panel de usuario

@login_required
def dashboard_logout(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect('index_views')  # URL para la página principal


@login_required
def create_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.user = request.user.userprofile
            item.save()
            return redirect('item_list')  # Redirige a la lista de ítems después de la creación
    else:
        item_form = ItemForm()

    return render(request, 'create_item.html', {'item_form': item_form})

@login_required
def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user.userprofile)

    if request.method == 'POST':
        item_form = ItemForm(request.POST, instance=item)
        if item_form.is_valid():
            item_form.save()
            return redirect('item_list')  # Redirige a la lista de ítems después de la actualización
    else:
        item_form = ItemForm(instance=item)

    return render(request, 'update_item.html', {'item_form': item_form})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user.userprofile)
    
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')  # Redirige a la lista de ítems después de la eliminación
    
    return render(request, 'delete_item.html', {'item': item})

def item_list(request):
    items = Item.objects.filter(user=request.user.userprofile)
    return render(request, 'item_list.html', {'items': items})

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user.userprofile
            post.save()
            return redirect('post_list')  # Redirige a la lista de publicaciones después de la creación
    else:
        post_form = PostForm()

    return render(request, 'create_post.html', {'post_form': post_form})

@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user.userprofile)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('post_list')  # Redirige a la lista de publicaciones después de la actualización
    else:
        post_form = PostForm(instance=post)

    return render(request, 'update_post.html', {'post_form': post_form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user.userprofile)
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')  # Redirige a la lista de publicaciones después de la eliminación
    
    return render(request, 'delete_post.html', {'post': post})

def post_list(request):
    posts = Post.objects.filter(user=request.user.userprofile)
    return render(request, 'post_list.html', {'posts': posts})

def post_main(request):
    posts = Post.objects.filter(user=request.user.userprofile)
    return render(request, 'post_main.html', {'posts': posts})

def item_main(request):
    posts = Post.objects.filter(user=request.user.userprofile)
    return render(request, 'item_main.html', {'posts': posts})