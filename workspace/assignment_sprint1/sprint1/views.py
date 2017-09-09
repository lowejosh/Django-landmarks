from django.shortcuts import render
from django.http import HttpResponse

# Index page view
def index(request):
    # Define the context of the python vars
    context_dict = { }
    # Return the template
    return render(request, 'publicMain.html', context=context_dict)

# Register page view
def register(request):
    # Define the context of the python vars
    context_dict = {'navBar': '<h5><a>Log in</a><br /><a>Register</a></h5>',
                    'contentBox': '<h1>Testing</h1>',
    }
    # Return the template
    return render(request, 'emptyTemplate.html', context=context_dict)
