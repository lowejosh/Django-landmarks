from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):

    # Define the context of the python vars
    context_dict = { }
    # Return the template
    return render(request, 'publicMain.html', context=context_dict)

