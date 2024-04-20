from django.shortcuts import render, redirect
from django.http import FileResponse
from .forms import FileUploadForm
from .models import UploadedFile

def upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('fileapp:download')
    else:
        form = FileUploadForm()
    return render(request, 'fileapp/upload.html', {'form': form})

def download(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    return render(request, 'fileapp/download.html', {'uploaded_file': uploaded_file})
