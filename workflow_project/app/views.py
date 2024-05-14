from django.shortcuts import render, redirect
from .forms import UserInputForm

def user_input(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = UserInputForm()
    return render(request, 'app/user_input.html', {'form': form})

def success(request):
    return render(request, 'app/success.html')
