from django.test import TestCase
from django.urls import reverse
from .models import Dropbox
from .forms import FileUploadForm, ExcelUploadForm
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class DropboxModelTests(TestCase):

    def setUp(self):
        # Setup a test file
        self.test_file = SimpleUploadedFile("test_file.csv", b"name,data\nJohn Doe,Sample data", content_type="text/csv")
        self.test_excel = SimpleUploadedFile("test_excel.xlsx", b"PK\x03\x04\x14\x00\x06\x00", content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
        # Create a Dropbox instance
        self.dropbox = Dropbox.objects.create(file=self.test_file, excel=self.test_excel)

    def test_file_creation(self):
        """Test the Dropbox instance is correctly created."""
        self.assertEqual(self.dropbox.file.name, "files/test_file.csv")
        self.assertEqual(self.dropbox.excel.name, "files/test_excel.xlsx")

class ViewResponseTests(TestCase):

    def test_task_file_list_view(self):
        """Test the TaskFileListView response status."""
        response = self.client.get(reverse('dropbox:task_file_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dropbox/task_file_list.html')

    def test_file_detail_view_get(self):
        """Test the FileDetailView GET method response."""
        response = self.client.get(reverse('dropbox:file_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dropbox/file_detail.html')

    def test_run_script_view_post(self):
        """Test the RunScriptView POST method."""
        # Assuming a Dropbox file exists
        self.test_file = SimpleUploadedFile("test_script.py", b"print('Hello, world!')", content_type="text/plain")
        dropbox = Dropbox.objects.create(file=self.test_file)
        response = self.client.post(reverse('dropbox:run_script'))
        self.assertEqual(response.status_code, 302)  # Redirect after post

    def test_download_view_get(self):
        """Test that the DownloadView returns the correct file type."""
        self.test_excel = SimpleUploadedFile("test_excel.xlsx", b"PK\x03\x04\x14\x00\x06\x00", content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        dropbox = Dropbox.objects.create(excel=self.test_excel)
        response = self.client.get(reverse('dropbox:download'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

class FormTests(TestCase):

    def test_file_upload_form(self):
        """Test the FileUploadForm validation and handling."""
        form_data = {'name': 'Test File'}
        form_files = {'file': SimpleUploadedFile("test_file.csv", b"name,data\nJohn Doe,Sample data", content_type="text/csv")}
        form = FileUploadForm(data=form_data, files=form_files)
        self.assertTrue(form.is_valid())

    def test_excel_upload_form(self):
        """Test the ExcelUploadForm validation and handling."""
        form_files = {'excel': SimpleUploadedFile("test_excel.xlsx", b"PK\x03\x04\x14\x00\x06\x00", content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        form = ExcelUploadForm(files=form_files)
        self.assertTrue(form.is_valid())
