from django.shortcuts import render
from django.http import HttpResponse
import subprocess

from .models import Dropbox

# Create your views here.
def file_list(request):
    files = Dropbox.objects.all()
    return render(request, 'dropbox/file_list.html', {'files': files})


def file_detail(request, file_id):
    return render(request, 'dropbox/file_detail.html')

def run_script(request):
    if request.method == 'POST':
        # Execute the Python script within the file_detail directory
        try:
            subprocess.run(['python', 'path/to/task_file/script.py'], check=True)
            return HttpResponse("Script executed successfully!")
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Error executing script: {e}", status=500)
    else:
        return HttpResponse("Method not allowed", status=405)