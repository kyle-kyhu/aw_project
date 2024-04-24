from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import FileResponse
import subprocess

from .models import Dropbox, Task_file
from .forms import FileUploadForm

from .models import xfile
from .forms import UploadXfileForm


def upload_xfile(request):
    if request.method == 'POST':
        form = UploadXfileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = xfile(name=request.FILES['file'].name, data=request.FILES['file'].read())
            instance.save()
            return redirect('dropbox:xfilelist')  # Redirect to the xfilelist page without passing any arguments
    else:
        form = UploadXfileForm()
    return render(request, 'dropbox/upload.html', {'form': form})

def xfilelist(request):
    files = xfile.objects.all()
    return render(request, 'dropbox/xfilelist.html', {'files': files})


def download_xfile(request, file_id):
    file = get_object_or_404(xfile, id=file_id)
    response = FileResponse(file.data, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={file.name}'
    return response


# view of task files
def task_file_list(request):
    tasks = Task_file.objects.all()
    files = Dropbox.objects.all()
    return render(request, 'dropbox/task_file_list.html', {'tasks': tasks, 'files': files})


def file_detail(request, file_id=None):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return redirect('dropbox:file_detail', file_id=instance.id)
    else:
        file = get_object_or_404(Dropbox, id=file_id) if file_id else None
        form = FileUploadForm()

    return render(request, 'dropbox/file_detail.html', {'form': form, 'file': file})


def download(request, file_id):
    uploaded_file = get_object_or_404(Dropbox, id=file_id)
    return render(request, 'dropbox/file_detail.html', {'uploaded_file': uploaded_file})


def run_script(request):
    if request.method == 'POST':
        file = request.FILES['file']
        dropbox = Dropbox(file=file)
        dropbox.save()

        # Execute the Python script within the file_detail directory
        try:
            subprocess.run(['python', 'files/sandbox1.py', dropbox.file.path], check=True)
            messages.success(request, "Script executed successfully!")
        except subprocess.CalledProcessError as e:
            messages.error(request, f"Error executing script: {e}")

        return redirect('dropbox:file_detail', file_id=dropbox.id)
    else:
        return HttpResponse("Method not allowed", status=405)


"""run script stand alone w/ message in view"""
# def run_script(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         dropbox = Dropbox(file=file)
#         dropbox.save()

#         # Execute the Python script within the file_detail directory
#         try:
#             subprocess.run(['python', 'files/sandbox1.py', dropbox.file.path], check=True)
#             return render(request, 'file_detail.html', {'file': dropbox, 'message': "Script executed successfully!"})
#         except subprocess.CalledProcessError as e:
#             return render(request, 'file_detail.html', {'file': dropbox, 'message': f"Error executing script: {e}"})
#     else:
#         return HttpResponse("Method not allowed", status=405)
    




"""run script within the file_detail"""
# def file_detail(request, file_id):
#     file = Dropbox.objects.get(id=file_id)

#     if request.method == 'POST':
#         if 'file' in request.FILES:
#             file.file = request.FILES['file']
#             file.save()
#         else:
#             # Execute the Python script within the file_detail directory
#             try:
#                 subprocess.run(['python', 'path/to/task_file/script.py', file.file.path], check=True)
#                 return HttpResponse(render(request, 'dropbox/file_detail.html', {'file': file, 'message': "Script executed successfully!"}))
#             except subprocess.CalledProcessError as e:
#                 return HttpResponse(render(request, 'dropbox/file_detail.html', {'file': file, 'message': f"Error executing script: {e}"}))

#     return render(request, 'dropbox/file_detail.html', {'file': file})