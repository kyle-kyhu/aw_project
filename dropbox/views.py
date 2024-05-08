

# from django.urls import reverse_lazy
# from django.contrib import messages
# from django.conf import settings
# from django.shortcuts import get_object_or_404, redirect
# from django.views.generic import ListView, View, FormView
# from django.http import HttpResponse
# import subprocess
# import os
# import glob

# from .models import Dropbox, Task_file
# from .forms import FileUploadForm, ExcelUploadForm

# '''classed based views'''

# class TaskFileListView(ListView):
#     template_name = 'dropbox/task_file_list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tasks'] = Task_file.objects.all()
#         context['files'] = Dropbox.objects.all()
#         return context

#     def get_queryset(self):
#         tasks = Task_file.objects.all()
#         files = Dropbox.objects.all()
#         return {'tasks': tasks, 'files': files}

# class FileDetailView(FormView):
#     template_name = 'dropbox/file_detail.html'
#     form_class = FileUploadForm
#     second_form_class = ExcelUploadForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         file_id = self.kwargs.get('file_id')
#         file_instance = get_object_or_404(Dropbox, id=file_id) if file_id else None
#         context.update({
#             'excel_form': self.second_form_class(self.request.POST or None),
#             'file': file_instance,
#             'show_run_script': self.request.session.pop('show_run_script', False),  # Pop is used here
#             'script_executed': self.request.session.get('script_executed', False)  # Get is used here
#         })
#         return context

#     def form_valid(self, form):
#         excel_form = self.second_form_class(self.request.POST, self.request.FILES)
#         if excel_form.is_valid():
#             csv_instance = form.save()
#             excel_instance = excel_form.save()
#             messages.success(self.request, "Your CSV and Excel files uploaded successfully!")
#             self.request.session['show_run_script'] = True  # Set the flag when files are saved
#             return redirect('dropbox:file_detail', file_id=csv_instance.id)
#         else:
#             messages.error(self.request, "Error uploading files. Please ensure both files are provided and try again.")
#             return self.form_invalid(form)

# class RunScriptView(View):
#     def post(self, request, *args, **kwargs):
#         dropbox = get_object_or_404(Dropbox, id=self.kwargs.get('file_id'))
#         if dropbox.file:
#             try:
#                 script_path = os.path.join(settings.MEDIA_ROOT, 'files/sandbox1.py')
#                 env = os.environ.copy()
#                 env['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
                
#                 # Run the Python script
#                 result = subprocess.run(['python', script_path, dropbox.file.path], check=True, env=env)
                
#                 if result.returncode == 0:  # Check if the script ran successfully
#                     messages.success(request, "Script executed successfully!")

#                     # Find the updated Excel file
#                     excel_files = glob.glob(os.path.join(settings.MEDIA_ROOT, 'files', '*.xlsx'))
#                     if excel_files:
#                         most_recent_excel_path = max(excel_files, key=os.path.getctime)
                        
#                         # Update the model's excel attribute
#                         dropbox.excel.name = os.path.basename(most_recent_excel_path)  # Use the file name directly
#                         dropbox.save()  # Save the model to update it in the database

#                     request.session['script_executed'] = True  # Set session flag for visibility
#             except subprocess.CalledProcessError as e:
#                 messages.error(request, f"Error executing script: {e}")
#         else:
#             messages.error(request, "No file has been uploaded.")
#         return redirect('dropbox:file_detail', file_id=self.kwargs.get('file_id'))


# class DownloadView(View):
#     def get(self, request, *args, **kwargs):
#         files_directory = os.path.join(os.getcwd(), 'media', 'files')
#         xlsx_files = glob.glob(os.path.join(files_directory, '*.xlsx'))
#         if xlsx_files:
#             most_recent_xlsx_file = max(xlsx_files, key=os.path.getctime)
#             with open(most_recent_xlsx_file, 'rb') as xlsx_file:
#                 response = HttpResponse(xlsx_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#                 response['Content-Disposition'] = f'attachment; filename="{os.path.basename(most_recent_xlsx_file)}"'
#                 return response
#         else:
#             messages.error(request, "No Excel files found in the media/files directory.")
#             return redirect('dropbox:file_detail', file_id=self.kwargs.get('file_id'))


from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View, FormView
from django.http import HttpResponse
import subprocess
import os
import glob

from .models import Dropbox, Task_file
from .forms import FileUploadForm, ExcelUploadForm

class TaskFileListView(ListView):
    template_name = 'dropbox/task_file_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task_file.objects.all()
        context['files'] = Dropbox.objects.all()
        return context

    def get_queryset(self):
        tasks = Task_file.objects.all()
        files = Dropbox.objects.all()
        return {'tasks': tasks, 'files': files}

class FileDetailView(FormView):
    template_name = 'dropbox/file_detail.html'
    form_class = FileUploadForm
    second_form_class = ExcelUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assume handling only the most recently uploaded or modified file
        file_instance = Dropbox.objects.last()  # Get the most recent file
        context.update({
            'excel_form': self.second_form_class(self.request.POST or None),
            'file': file_instance,
            'show_run_script': self.request.session.pop('show_run_script', False),
            'script_executed': self.request.session.get('script_executed', False)
        })
        return context

    def form_valid(self, form):
        excel_form = self.second_form_class(self.request.POST, self.request.FILES)
        if excel_form.is_valid():
            csv_instance = form.save()
            excel_instance = excel_form.save()
            messages.success(self.request, "Your CSV and Excel files uploaded successfully!")
            self.request.session['show_run_script'] = True
            return redirect('dropbox:file_detail')
        else:
            messages.error(self.request, "Error uploading files. Please ensure both files are provided and try again.")
            return self.form_invalid(form)

class RunScriptView(View):
    def post(self, request, *args, **kwargs):
        dropbox = Dropbox.objects.last()  # Handle the most recent file
        if dropbox and dropbox.file:
            try:
                script_path = os.path.join(settings.MEDIA_ROOT, 'files/sandbox1.py')
                env = os.environ.copy()
                env['DJANGO_SETTINGS_MODULE'] = 'django_project.settings'
                # run the python file
                result = subprocess.run(['python', script_path, dropbox.file.path], check=True, env=env)
                if result.returncode == 0:
                    messages.success(request, "Script executed successfully!")
                    excel_files = glob.glob(os.path.join(settings.MEDIA_ROOT, 'files', '*.xlsx'))
                    if excel_files:
                        most_recent_excel_path = max(excel_files, key=os.path.getctime)
                        dropbox.excel.name = os.path.basename(most_recent_excel_path)
                        dropbox.save()
                    request.session['script_executed'] = True
            except subprocess.CalledProcessError as e:
                messages.error(request, f"Error executing script: {e}")
        else:
            messages.error(request, "No file has been uploaded.")
        return redirect('dropbox:file_detail')

class DownloadView(View):
    def get(self, request, *args, **kwargs):
        files_directory = os.path.join(os.getcwd(), 'media', 'files')
        xlsx_files = glob.glob(os.path.join(files_directory, '*.xlsx'))
        if xlsx_files:
            most_recent_xlsx_file = max(xlsx_files, key=os.path.getctime)
            with open(most_recent_xlsx_file, 'rb') as xlsx_file:
                response = HttpResponse(xlsx_file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(most_recent_xlsx_file)}"'
                return response
        else:
            messages.error(request, "No Excel files found in the media/files directory.")
            return redirect('dropbox:file_detail')
