from django.shortcuts import render
from django.http import HttpResponse

# Index page view
def index(request):
    # Define the context of the python vars
    context_dict = { }
    # Return the template
    return render(request, 'publicMain.html', context=context_dict)

# --OLD--  Register page view
def register(request):
    # Define the context of the python vars
    context_dict = {'navBar': '<h5><a>Log in</a><br /><a>Register</a></h5>', }
    # Return the template
    return render(request, 'base.html', context=context_dict)

# --NEW-- Signup page view
def signup(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


