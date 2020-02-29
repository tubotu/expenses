from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ItemForm
from django.contrib import messages

def index(request):
    return render(request, 'app/index.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            input_user_name = form.cleaned_data['user_name']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(email=input_email, password=input_password)
        if new_user is not None:
            login(request, new_user)
            return redirect('app:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

@login_required
def items_new(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        print(form)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, "投稿が完了しました！")
        return redirect('app:index')     
    else:          
        form = ItemForm()
    return render(request, 'app/items_new.html', {'form': form})