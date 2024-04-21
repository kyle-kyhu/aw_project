from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import subprocess

from .models import Dropbox
from .forms import FileUploadForm

# view of task files
def file_list(request):
    files = Dropbox.objects.all()
    return render(request, 'dropbox/file_list.html', {'files': files})


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
    
from django.shortcuts import redirect

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