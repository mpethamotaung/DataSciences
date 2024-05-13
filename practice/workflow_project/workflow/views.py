from django.shortcuts import render
from .models import Workflow

# Create your views here.
def workflow_list(request):
    workflows = Workflow_objects.all()
    return render(request, 'workflow/workflow_list.html', {'workflows': workflows})