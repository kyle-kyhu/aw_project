from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
import subprocess
import os
import glob

from .models import Dropbox, Task_file
from .forms import FileUploadForm, ExcelUploadForm


# Kyle's view 
def task_file_list(request): 
    tasks = Task_file.objects.all()
    files = Dropbox.objects.all()
    return render(request, 'dropbox/task_file_list.html', {'tasks': tasks, 'files': files})

def file_detail(request, file_id=None):
    file = get_object_or_404(Dropbox, id=file_id) if file_id else None

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        excel_form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid() and excel_form.is_valid():
            csv_instance = form.save()
            excel_instance = excel_form.save()
            messages.success(request, "Your CSV and Excel files uploaded successfully!")
            return redirect('dropbox:run_script', file_id=csv_instance.id)
        else:
            messages.error(request, "Error uploading files. Please ensure both files are provided and try again.")
    else:
        form = FileUploadForm()
        excel_form = ExcelUploadForm()

    return render(request, 'dropbox/file_detail.html', {'form': form, 'excel_form': excel_form, 'file': file})

def run_script(request, file_id):
    dropbox = get_object_or_404(Dropbox, id=file_id)
    if request.method == 'POST':
        if dropbox.file:  # Check if a file has been uploaded
            try:
                # Run the Python script with the uploaded CSV file path
                script_path = os.path.join(settings.MEDIA_ROOT, 'files/sandbox1.py')
                env = os.environ.copy()
                env['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
                subprocess.run(['python', script_path, dropbox.file.path], check=True, env=env)
                messages.success(request, "Yay!  The script executed successfully!")
            except subprocess.CalledProcessError as e:
                messages.error(request, f"Error executing script: {e}")
        else:
            messages.error(request, "No file has been uploaded.")
    else:
        messages.error(request, "Method not allowed")
    # Redirect back to the file detail view
    return redirect('dropbox:file_detail', file_id=file_id)


def download(request, file_id):
    # Get the path to the media/files directory
    files_directory = os.path.join(os.getcwd(), 'media', 'files')

    # Find any Excel file in the media/files directory
    xlsx_files = glob.glob(os.path.join(files_directory, '*.xlsx'))

    if xlsx_files:
        # Get the most recent Excel file based on creation time
        most_recent_xlsx_file = max(xlsx_files, key=os.path.getctime)

        # Open the most recent Excel file in binary mode
        with open(most_recent_xlsx_file, 'rb') as xlsx_file:
            # Return a response with the file to trigger the download
            response = HttpResponse(xlsx_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(most_recent_xlsx_file)}"'
            return response
    else:
        messages.error(request, "No Excel files found in the media/files directory.")
        return redirect('dropbox:file_detail', file_id=file_id)


# def success_view(request):
#     return render(request, 'dropbox/success.html')
